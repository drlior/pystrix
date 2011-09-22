"""
pystrix.ami.core_events
=======

Provides defnitions and filtering rules for events that may be raised by Asterisk.

Legal
-----

This file is part of pystrix.
pystrix is free software; you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published
by the Free Software Foundation; either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU General Public License and
GNU Lesser General Public License along with this program. If not, see
<http://www.gnu.org/licenses/>.

(C) Ivrnet, inc., 2011

Authors:

- Neil Tallim <n.tallim@ivrnet.com>

The events implemented by this module follow the definitions provided by
http://www.asteriskdocs.org/ and https://wiki.asterisk.org/
"""
from ami import _Message

class DBGetResponse(_Message):
    """
    Provides the value requested from the database.
    
    - 'Family' : The family of the value being provided
    - 'Key' : The key of the value being provided
    - 'Val' : The value being provided, represented as a string
    """

class FullyBooted(_Message):
    """
    Indicates that Asterisk is online.
    
    - 'Status' : "Fully Booted"
    """
    
class Hangup(_Message):
    """
    Indicates that a channel has been hung up.
    
    - 'Cause' : One of the following numeric values, as a string:
    
     - '0' : Channel cleared normally
     
    - 'Cause-txt' : Additional information related to the hangup
    - 'Channel' : The channel hung-up
    - 'Uniqueid' : An Asterisk unique value
    """
    def process(self):
        """
        Translates the 'Cause' header's value into an int, setting it to `None` if coercion fails.
        """
        (headers, data) = _Message.process(self)
        try:
            headers['Cause'] = int(headers['Cause'])
        except Exception:
            headers['Cause'] = None
        return (headers, data)
        
class ParkedCall(_Message):
    """
    Describes a parked call.
    
    - 'ActionID' : The ID associated with the original request
    - 'CallerID' : The ID of the caller, ".+?" <.+?>
    - 'CallerIDName' (optional) : The name of the caller, on supporting channels
    - 'Channel' : The channel of the parked call
    - 'Exten' : The extension associated with the parked call
    - 'From' : The callback channel associated with the call
    - 'Timeout' (optional) : The time remaining before the call is reconnected with the callback
                             channel
    """
    def process(self):
        """
        Translates the 'Timeout' header's value into an int, setting it to `None` if coercion
        fails, and leaving it absent if it wasn't present in the original response.
        """
        (headers, data) = _Message.process(self)
        timeout = headers.get('Timeout')
        if not timeout is None:
            try:
                headers['Timeout'] = int(timeout)
            except Exception:
                headers['Timeout'] = None
        return (headers, data)
        
class ParkedCallsComplete(_Message):
    """
    Indicates that all parked calls have been listed.
    
    - 'ActionID' : The ID associated with the original request
    """

class PeerEntry(_Message):
    """
    Describes a peer.
    
    - 'ActionID' : The ID associated with the original request
    - 'ChannelType' : The type of channel being described.
    
     - 'SIP'
     
    - 'ObjectName' : The internal name by which this peer is known
    - 'ChanObjectType': The type of object
    
     - 'peer'
     
    - 'IPaddress' (optional) : The IP of the peer
    - 'IPport' (optional) : The port of the peer
    - 'Dynamic' : 'yes' or 'no', depending on whether the peer is resolved by IP or authentication
    - 'Natsupport' : 'yes' or 'no', depending on whether the peer's messages' content should be
                     trusted for routing purposes. If not, packets are sent back to the last hop
    - 'VideoSupport' : 'yes' or 'no'
    - 'ACL' : 'yes' or 'no'
    - 'Status' : 'Unmonitored', 'OK (\d+ ms)'
    - 'RealtimeDevice' : 'yes' or 'no'
    """
    def process(self):
        """
        Translates the 'Port' header's value into an int, setting it to `None` if coercion
        fails, and leaving it absent if it wasn't present in the original response.
        
        Translates the 'Dynamic', 'Natsupport', 'VideoSupport', 'ACL', and 'RealtimeDevice' headers'
        values into bools.
        """
        (headers, data) = _Message.process(self)
        
        ip_port = headers.get('IPport')
        if not ip_port is None:
            try:
                headers['IPport'] = int(ip_port)
            except Exception:
                headers['IPport'] = None
                
        for header in ('Dynamic', 'Natsupport', 'VideoSupport', 'ACL', 'RealtimeDevice'):
            headers[header] = headers.get(header) == 'yes'
            
        return (headers, data)

class PeerlistComplete(_Message):
    """
    Indicates that all peers have been listed.
    
    - 'ActionID' : The ID associated with the original request
    """

class QueueEntry(_Message):
    """
    Indicates that a call is waiting to be answered.
    
    - 'ActionID' (optional) : The ID associated with the original request, if a response
    - 'Channel' : The channel of the inbound call
    - 'CallerID' : The (often) numeric ID of the caller
    - 'CallerIDName' (optional) : The friendly name of the caller on supporting channels
    - 'Position' : The numeric position of the caller in the queue
    - 'Queue' : The queue in which the caller is waiting
    - 'Wait' : The number of seconds the caller has been waiting
    """
    def process(self):
        """
        Translates the 'Position' and 'Wait' headers' values into ints, setting them to -1 on error.
        """
        (headers, data) = _Message.process(self)
        for header in ('Position', 'Wait'):
            try:
                headers[header] = int(headers.get(header))
            except Exception:
                headers[header] = -1
        return (headers, data)

class QueueMember(_Message):
    """
    Describes a member of a queue.
    
    - 'ActionID' (optional) : The ID associated with the original request, if a response
    - 'CallsTaken' : The number of calls received by this member
    - 'LastCall' : The UNIX timestamp of the last call taken, or 0 if none
    - 'Location' : The interface in the queue
    - 'MemberName' (optional) : The friendly name of the member
    - 'Membership' : "dynamic" ("static", too?)
    - 'Paused' : '1' or '0' for 'true' and 'false', respectively
    - 'Penalty' : The selection penalty to apply to this member (higher numbers mean later selection)
    - 'Queue' : The queue to which the member belongs
    - 'Status' : One of the following, as a string:
    
     - '0' : Idle
     - '1' : In use
     - '2' : Busy
    """
    def process(self):
        """
        Translates the 'CallsTaken', 'LastCall', 'Penalty', and 'Status' headers' values into ints,
        setting them to -1 on error.
        
        'Paused' is set to a bool.
        """
        (headers, data) = _Message.process(self)
        
        for header in ('CallsTaken', 'LastCall', 'Penalty', 'Status'):
            try:
                headers[header] = int(headers.get(header))
            except Exception:
                headers[header] = -1
                
        paused = headers.get('Paused')
        headers['Paused'] = paused and paused == '1'
        
        return (headers, data)
        
class QueueMemberAdded(_Message):
    """
    Indicates that a member was added to a queue.
    
    - 'CallsTaken' : The number of calls received by this member
    - 'LastCall' : The UNIX timestamp of the last call taken, or 0 if none
    - 'Location' : The interface added to the queue
    - 'MemberName' (optional) : The friendly name of the member
    - 'Membership' : "dynamic" ("static", too?)
    - 'Paused' : '1' or '0' for 'true' and 'false', respectively
    - 'Penalty' : The selection penalty to apply to this member (higher numbers mean later selection)
    - 'Queue' : The queue to which the member was added
    - 'Status' : One of the following, as a string:
    
     - '0' : Idle
     - '1' : In use
     - '2' : Busy
    """
    def process(self):
        """
        Translates the 'CallsTaken', 'LastCall', 'Penalty', and 'Status' headers' values into ints,
        setting them to -1 on error.
        
        'Paused' is set to a bool.
        """
        (headers, data) = _Message.process(self)
        
        for header in ('CallsTaken', 'LastCall', 'Penalty', 'Status'):
            try:
                headers[header] = int(headers.get(header))
            except Exception:
                headers[header] = -1
                
        paused = headers.get('Paused')
        headers['Paused'] = paused and paused == '1'
        
        return (headers, data)
        
class QueueMemberPaused(_Message):
    """
    Indicates that the pause-state of a queue member was changed.
    
    - 'Location' : The interface added to the queue
    - 'MemberName' (optional) : The friendly name of the member
    - 'Paused' : '1' or '0' for 'true' and 'false', respectively
    - 'Queue' : The queue in which the member was paused
    """
    def process(self):
        """
        'Paused' is set to a bool.
        """
        (headers, data) = _Message.process(self)
        paused = headers.get('Paused')
        headers['Paused'] = paused and paused == '1'
        return (headers, data)

class QueueMemberRemoved(_Message):
    """
    Indicates that a member was removed from a queue.
    
    - 'Location' : The interface removed from the queue
    - 'MemberName' (optional) : The friendly name of the member
    - 'Queue' : The queue from which the member was removed
    """
    
class QueueParams(_Message):
    """
    Describes the attributes of a queue.
    
    - 'Abandoned' : The number of calls that have gone unanswered
    - 'ActionID' (optional) : The ID associated with the original request, if a response
    - 'Calls' : The number of current calls in the queue
    - 'Completed' : The number of completed calls
    - 'Holdtime' : ?
    - 'Max' : ?
    - 'Queue' : The queue being described
    - 'ServiceLevel' : ?
    - 'ServiceLevelPerf' : ?
    - 'Weight' : ?
    """
    def process(self):
        """
        Translates the 'Abandoned', 'Calls', 'Completed', 'Holdtime', and 'Max' headers' values into
        ints, setting them to -1 on error.
        
        Translates the 'ServiceLevel', 'ServiceLevelPerf', and 'Weight' values into
        floats, setting them to None on error.
        """
        (headers, data) = _Message.process(self)
        
        for header in ('Abandoned', 'Calls', 'Completed', 'Holdtime', 'Max'):
            try:
                headers[header] = int(headers.get(header))
            except Exception:
                headers[header] = -1
                
        for header in ('ServiceLevel', 'ServiceLevelPerf', 'Weight'):
            try:
                headers[header] = float(headers.get(header))
            except Exception:
                headers[header] = -1
        
        return (headers, data)
        
class QueueStatusComplete(_Message):
    """
    Indicates that a QueueStatus request has completed.
    
    - 'ActionID' : The ID associated with the original request
    """
    
class Status(_Message):
    """
    Describes the current status of a channel.
    
    - 'Account' : The billing account associated with the channel; may be empty
    - 'ActionID' : The ID associated with the original request
    - 'Channel' : The channel being described
    - 'CallerID' : The ID of the caller, ".+?" <.+?>
    - 'CallerIDNum' : The (often) numeric component of the CallerID
    - 'CallerIDName' (optional) : The, on suporting channels, name of the caller, enclosed in quotes
    - 'Context' : The context of the directive the channel is executing
    - 'Extension' : The extension of the directive the channel is executing
    - 'Link' : ?
    - 'Priority' : The priority of the directive the channel is executing
    - 'Seconds' : The number of seconds the channel has been active
    - 'State' : "Up"
    - 'Uniqueid' : An Asterisk unique value
    """
    def process(self):
        """
        Translates the 'Seconds' header's value into an int, setting it to -1 on error.
        """
        (headers, data) = _Message.process(self)
        try:
            headers['Seconds'] = int(headers.get('Seconds'))
        except Exception:
            headers['Seconds'] = -1
        return (headers, data)
        
class StatusComplete(_Message):
    """
    Indicates that all requested channel information has been provided.
    
    - 'ActionID' : The ID associated with the original request
    """

class UserEvent(_Message):
    """
    Generated in response to the UserEvent request.
    
    - 'ActionID' : The ID associated with the original request
    - \* : Any key-value pairs supplied with the request, as strings
    """

class VarSet(_Message):
    """
    Emitted when a variable is set, either globally or on a channel.
    
    - 'Channel' (optional) : The channel on which the variable was set, if not global
    - 'Uniqueid' : An Asterisk unique value
    - 'Value' : The value of the variable, as a string
    - 'Variable' : The name of the variable that was set
    """

