/*
 * meta: title - Stateless Packet Filtering Profile
 * meta: package - http://oasis-open.org/openc2/oc2slpf/v1.1
 * meta: version - 0-wd01
 * meta: description - Data definitions for Stateless Packet Filtering (SLPF) functions
 * meta: exports - ["OpenC2-Command", "OpenC2-Response"]
 * meta: config - {}
*/


struct OpenC2-Command { // $Record #options:{}
  1:  required  Action      action;      // The task or activity to be performed $Action #options:{}                      
  2:  required  Target      target;      // The object referenced by the Action $Target #options:{}                       
  3:  optional  Args        args;        // Additional information that applies to the Command $Args #options:{"minc": 0} 
  4:  optional  Actuator    actuator;    // The profile that defines the Command $Actuator #options:{"minc": 0}           
  5:  optional  Command-ID  command_id;  // An identifier of this Command $Command-ID #options:{"minc": 0}                
}


struct OpenC2-Response { // $Map #options:{}
  1:  optional  Status-Code  status;       // Integer status code $Status-Code #options:{}                              
  2:  optional  string       status_text;  // Free-form description of the Response status $String #options:{"minc": 0} 
  3:  optional  Results      results;      // Results returned by the invoked Command $Results #options:{"minc": 0}     
}


enum Action { // Actions used in this profile $Enumerated #options:{}
  query =   3;   // Initiate a request for information                                                                                                     
  deny =    6;   // Prevent a certain event or action from completion, such as preventing a flow from reaching a destination or preventing access          
  allow =   8;   // Permit access to or execution of a Target                                                                                              
  update =  16;  // Instruct a component to retrieve, install, process, and operate in accordance with a software update, reconfiguration, or other update 
  delete =  20;  // Remove an entity (e.g., data, files, flows)                                                                                            
}


struct Target { // Targets used in this profile $Choice #options:{}
  9:     optional  Features         features;         // A set of items used with the query Action to determine an Actuator's capabilities $Features #options:{}                          
  10:    optional  File             file;             // Properties of a file $File #options:{}                                                                                           
  13:    optional  IPv4-Net         ipv4_net;         // An IPv4 address range including CIDR prefix length $IPv4-Net #options:{}                                                         
  14:    optional  IPv6-Net         ipv6_net;         // An IPv6 address range including prefix length $IPv6-Net #options:{}                                                              
  15:    optional  IPv4-Connection  ipv4_connection;  // A 5-tuple of source and destination IPv4 address ranges, source and destination ports, and protocol $IPv4-Connection #options:{} 
  16:    optional  IPv6-Connection  ipv6_connection;  // A 5-tuple of source and destination IPv6 address ranges, source and destination ports, and protocol $IPv6-Connection #options:{} 
  1024:  optional  AP-Target        slpf;             // Targets defined in this profile $AP-Target #options:{"dir": true}                                                                
}


struct Actuator { // $Map #options:{"minv": 1}
  1024:  optional  AP-Specifiers  slpf;  // Actuator Specifiers defined in this profile $AP-Specifiers #options:{"minc": 0, "dir": true} 
}


struct Args { // $Map #options:{"minv": 1}
  1:     optional  Date-Time      start_time;          // The specific date/time to initiate the Command $Date-Time #options:{"minc": 0}                                 
  2:     optional  Date-Time      stop_time;           // The specific date/time to terminate the Command $Date-Time #options:{"minc": 0}                                
  3:     optional  Duration       duration;            // The length of time for an Command to be in effect $Duration #options:{"minc": 0}                               
  4:     optional  Response-Type  response_requested;  // The type of Response required for the Command: none, ack, status, complete $Response-Type #options:{"minc": 0} 
  1024:  optional  AP-Args        slpf;                // Command Arguments defined in this profile $AP-Args #options:{"minc": 0, "dir": true}                           
}


struct Results { // Response Results $Map #options:{"minv": 1}
  1:     optional  Results$Versions    versions;    // List of OpenC2 language versions supported by this Actuator $Results$Versions #options:{"minc": 0}           
  2:     optional  Results$Profiles    profiles;    // List of profiles supported by this Actuator $Results$Profiles #options:{"minc": 0}                           
  3:     optional  Action-Targets      pairs;       // List of targets applicable to each supported Action $Action-Targets #options:{"minc": 0}                     
  4:     optional  Results$rate-limit  rate_limit;  // Maximum number of requests per minute supported by design or policy $Results$rate-limit #options:{"minc": 0} 
  5:     optional  Results$Args        args;        // List of supported Command Arguments $Results$Args #options:{"minc": 0}                                       
  1024:  optional  AP-Results          slpf;        // Results defined in this profile $AP-Results #options:{"minc": 0, "dir": true}                                
}


struct Action-Targets { // Targets applicable to each action $Map #options:{}
  3:   optional  Action-targets$Query   query;   // $Action-targets$Query #options:{}  
  6:   optional  Action-targets$Deny    deny;    // $Action-targets$Deny #options:{}   
  8:   optional  Action-targets$Allow   allow;   // $Action-targets$Allow #options:{}  
  16:  optional  Action-targets$Update  update;  // $Action-targets$Update #options:{} 
  20:  optional  Action-targets$Delete  delete;  // $Action-targets$Delete #options:{} 
}


enum Query-Targets { // $Enumerated #options:{}
  features =  1;  // 
}


enum Allow-Deny-Targets { // $Enumerated #options:{}
  ipv4_net =         1;  // 
  ipv6_net =         2;  // 
  ipv4_connection =  3;  // 
  ipv6_connection =  4;  // 
}


enum Update-Targets { // $Enumerated #options:{}
  file =  1;  // 
}


enum Delete-Targets { // $Enumerated #options:{}
  slpf/rule_number =  1;  // 
}


struct AP-Target { // SLPF targets $Choice #options:{}
  1:  optional  Rule-ID  rule_number;  // Immutable identifier assigned when a rule is created. Identifies a rule to be deleted $Rule-ID #options:{} 
}


struct AP-Specifiers { // SLPF actuator specifiers (may be empty) $Map #options:{}
  1:  optional  string                     hostname;     // RFC 1123 hostname (can be a domain name or IP address) for a particular device with SLPF functionality $String #options:{"minc": 0}    
  2:  optional  string                     named_group;  // User defined collection of devices with SLPF functionality $String #options:{"minc": 0}                                                
  3:  optional  string                     asset_id;     // Unique identifier for a particular SLPF $String #options:{"minc": 0}                                                                   
  4:  optional  Ap-specifiers$Asset_tuple  asset_tuple;  // Unique tuple identifier for a particular SLPF consisting of a list of up to 10 strings $Ap-specifiers$Asset_tuple #options:{"minc": 0} 
}


struct AP-Args { // SLPF command arguments $Map #options:{"minv": 1}
  1:  optional  Drop-Process  drop_process;  // Specifies how to handle denied packets $Drop-Process #options:{"minc": 0}                                                                                                                                                                  
  2:  optional  bool          persistent;    // Normal operations assume any changes to a device are to be implemented persistently. Setting the persistent modifier to FALSE results in a change that is not persistent in the event of a reboot or restart $Boolean #options:{"minc": 0} 
  3:  optional  Direction     direction;     // Specifies whether to apply rules to incoming or outgoing traffic. If omitted, rules are applied to both $Direction #options:{"minc": 0}                                                                                                    
  4:  optional  Rule-ID       insert_rule;   // Specifies the identifier of the rule within a list, typically used in a top-down rule list $Rule-ID #options:{"minc": 0}                                                                                                                   
}


struct AP-Results { // SLPF results defined in this profile $Map #options:{}
  1:  optional  Rule-ID  rule_number;  // Rule identifier returned from allow or deny Command. $Rule-ID #options:{"minc": 0} 
}


enum Drop-Process { // $Enumerated #options:{}
  none =       1;  // Drop the packet and do not send a notification to the source of the packet                    
  reject =     2;  // Drop the packet and send an ICMP host unreachable (or equivalent) to the source of the packet 
  false_ack =  3;  // Drop the traffic and send a false acknowledgement                                             
}


enum Direction { // $Enumerated #options:{}
  both =     1;  // Apply rules to all traffic           
  ingress =  2;  // Apply rules to incoming traffic only 
  egress =   3;  // Apply rules to outgoing traffic only 
}

// Rule-ID(Integer)

enum Status-Code { // $Enumerated #options:{"id": true}
  Processing =           102;  // an interim Response used to inform the Producer that the Consumer has accepted the Command but has not yet completed it                            
  OK =                   200;  // the Command has succeeded                                                                                                                          
  Created =              201;  // the Command has succeeded and a new resource has been created as a result of it                                                                    
  Bad_Request =          400;  // the Consumer cannot process the Command due to something that is perceived to be a Producer error (e.g., malformed Command syntax)                 
  Unauthorized =         401;  // the Command Message lacks valid authentication credentials for the target resource or authorization has been refused for the submitted credentials 
  Forbidden =            403;  // the Consumer understood the Command but refuses to authorize it                                                                                    
  Not_Found =            404;  // the Consumer has not found anything matching the Command                                                                                           
  Internal_Error =       500;  // the Consumer encountered an unexpected condition that prevented it from performing the Command                                                     
  Not_Implemented =      501;  // the Consumer does not support the functionality required to perform the Command                                                                    
  Service_Unavailable =  503;  // the Consumer is currently unable to perform the Command due to a temporary overloading or maintenance of the Consumer                              
}


struct Features {
  1: optional list<string> item; // An array of zero to ten names used to query an Actuator for its supported capabilities. $ArrayOf #options:{"vtype": "Feature", "maxv": 10, "unique": true}
}


struct File { // $Map #options:{"minv": 1}
  1:  optional  string  name;    // The name of the file as defined in the file system $String #options:{"minc": 0}               
  2:  optional  string  path;    // The absolute path to the location of the file in the file system $String #options:{"minc": 0} 
  3:  optional  Hashes  hashes;  // One or more cryptographic hash codes of the file contents $Hashes #options:{"minc": 0}        
}


struct IPv4-Net {
  1: optional list<string> item; // IPv4 address and prefix length $Array #options:{"format": "ipv4-net"}
}


struct IPv4-Connection { // 5-tuple that specifies a tcp/ip connection $Record #options:{"minv": 1}
  1:  optional  IPv4-Net     src_addr;  // IPv4 source address range $IPv4-Net #options:{"minc": 0}                                 
  2:  optional  Port         src_port;  // Source service per [RFC6335] $Port #options:{"minc": 0}                                  
  3:  optional  IPv4-Net     dst_addr;  // IPv4 destination address range $IPv4-Net #options:{"minc": 0}                            
  4:  optional  Port         dst_port;  // Destination service per [RFC6335] $Port #options:{"minc": 0}                             
  5:  optional  L4-Protocol  protocol;  // Layer 4 protocol (e.g., TCP) - see L4-Protocol section $L4-Protocol #options:{"minc": 0} 
}


struct IPv6-Net {
  1: optional list<string> item; // IPv6 address and prefix length $Array #options:{"format": "ipv6-net"}
}


struct IPv6-Connection { // 5-tuple that specifies a tcp/ip connection $Record #options:{"minv": 1}
  1:  optional  IPv6-Net     src_addr;  // IPv6 source address range $IPv6-Net #options:{"minc": 0}                            
  2:  optional  Port         src_port;  // Source service per [RFC6335] $Port #options:{"minc": 0}                             
  3:  optional  IPv6-Net     dst_addr;  // IPv6 destination address range $IPv6-Net #options:{"minc": 0}                       
  4:  optional  Port         dst_port;  // Destination service per [RFC6335] $Port #options:{"minc": 0}                        
  5:  optional  L4-Protocol  protocol;  // Layer 4 protocol (e.g., TCP) - [Section 3.4.2.10] $L4-Protocol #options:{"minc": 0} 
}

// Date-Time(Integer)
// Duration(Integer)

enum Feature { // Specifies the results to be returned from a query features Command $Enumerated #options:{}
  versions =    1;  // List of OpenC2 Language versions supported by this Actuator         
  profiles =    2;  // List of profiles supported by this Actuator                         
  pairs =       3;  // List of supported Actions and applicable Targets                    
  rate_limit =  4;  // Maximum number of Commands per minute supported by design or policy 
  args =        5;  // List of supported Command Argumemnts                                
}


struct Hashes { // Cryptographic hash values $Map #options:{"minv": 1}
  1:  optional  Hashes$md5     md5;     // MD5 hash as defined in [RFC1321] $Hashes$md5 #options:{}       
  2:  optional  Hashes$sha1    sha1;    // SHA1 hash as defined in [RFC6234] $Hashes$sha1 #options:{}     
  3:  optional  Hashes$sha256  sha256;  // SHA256 hash as defined in [RFC6234] $Hashes$sha256 #options:{} 
}

// IPv4-Addr(Binary)
// IPv6-Addr(Binary)

enum L4-Protocol { // Value of the protocol (IPv4) or next header (IPv6) field in an IP packet. Any IANA value, [RFC5237] $Enumerated #options:{}
  icmp =  1;    // Internet Control Message Protocol - [RFC0792]    
  tcp =   6;    // Transmission Control Protocol - [RFC0793]        
  udp =   17;   // User Datagram Protocol - [RFC0768]               
  sctp =  132;  // Stream Control Transmission Protocol - [RFC4960] 
}

// Port(Integer)

enum Response-Type { // $Enumerated #options:{}
  none =      0;  // No response                                     
  ack =       1;  // Respond when Command received                   
  status =    2;  // Respond with progress toward Command completion 
  complete =  3;  // Respond when all aspects of Command completed   
}

// Version(String)
// Namespace(String)
// Command-ID(String)

struct Results$Versions {
  1: optional list<string> item; // List of OpenC2 language versions supported by this Actuator $ArrayOf #options:{"vtype": "Version", "minv": 1, "maxv": 10, "unique": true}
}


struct Results$Profiles {
  1: optional list<string> item; // List of profiles supported by this Actuator $ArrayOf #options:{"vtype": "Namespace", "minv": 1, "unique": true}
}


struct Results$Args {
  1: optional list<string> item; // List of supported Command Arguments $ArrayOf #options:{"vtype": "Enumerated", "minv": 1}
}


struct Action-targets$Query {
  1: optional list<string> item; // $ArrayOf #options:{"vtype": "Query-Targets", "minv": 1, "maxv": 10, "unique": true}
}


struct Action-targets$Deny {
  1: optional list<string> item; // $ArrayOf #options:{"vtype": "Allow-Deny-Targets", "minv": 1, "maxv": 10, "unique": true}
}


struct Action-targets$Allow {
  1: optional list<string> item; // $ArrayOf #options:{"vtype": "Allow-Deny-Targets", "minv": 1, "maxv": 10, "unique": true}
}


struct Action-targets$Update {
  1: optional list<string> item; // $ArrayOf #options:{"vtype": "Update-Targets", "minv": 1, "maxv": 10, "unique": true}
}


struct Action-targets$Delete {
  1: optional list<string> item; // $ArrayOf #options:{"vtype": "Delete-Targets", "minv": 1, "maxv": 10, "unique": true}
}


struct Ap-specifiers$Asset_tuple {
  1: optional list<string> item; // Unique tuple identifier for a particular SLPF consisting of a list of up to 10 strings $ArrayOf #options:{"vtype": "String", "minv": 1, "maxv": 10}
}

// Results$rate-limit(Number)
// Hashes$md5(Binary)
// Hashes$sha1(Binary)
// Hashes$sha256(Binary)
