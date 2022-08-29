/*
 * meta: title - Stateless Packet Filtering Profile
 * meta: package - http://oasis-open.org/openc2/oc2slpf/v1.1
 * meta: version - 0-wd01
 * meta: description - Data definitions for Stateless Packet Filtering (SLPF) functions
 * meta: exports - ["OpenC2-Command", "OpenC2-Response"]
 * meta: config - {}
*/


struct OpenC2-Command { 
  1:  required  Action      action;       
  2:  required  Target      target;       
  3:  optional  Args        args;         
  4:  optional  Actuator    actuator;     
  5:  optional  Command-ID  command_id;   
}


struct OpenC2-Response { 
  1:  optional  Status-Code  status;        
  2:  optional  string       status_text;   
  3:  optional  Results      results;       
}


enum Action { 
  query =   3;    
  deny =    6;    
  allow =   8;    
  update =  16;   
  delete =  20;   
}


struct Target { 
  9:     optional  Features         features;          
  10:    optional  File             file;              
  13:    optional  IPv4-Net         ipv4_net;          
  14:    optional  IPv6-Net         ipv6_net;          
  15:    optional  IPv4-Connection  ipv4_connection;   
  16:    optional  IPv6-Connection  ipv6_connection;   
  1024:  optional  AP-Target        slpf;              
}


struct Actuator { 
  1024:  optional  AP-Specifiers  slpf;   
}


struct Args { 
  1:     optional  Date-Time      start_time;           
  2:     optional  Date-Time      stop_time;            
  3:     optional  Duration       duration;             
  4:     optional  Response-Type  response_requested;   
  1024:  optional  AP-Args        slpf;                 
}


struct Results { 
  1:     optional  Results$Versions    versions;     
  2:     optional  Results$Profiles    profiles;     
  3:     optional  Action-Targets      pairs;        
  4:     optional  Results$rate-limit  rate_limit;   
  5:     optional  Results$Args        args;         
  1024:  optional  AP-Results          slpf;         
}


struct Action-Targets { 
  3:   optional  Action-targets$Query   query;    
  6:   optional  Action-targets$Deny    deny;     
  8:   optional  Action-targets$Allow   allow;    
  16:  optional  Action-targets$Update  update;   
  20:  optional  Action-targets$Delete  delete;   
}


enum Query-Targets { 
  features =  1;   
}


enum Allow-Deny-Targets { 
  ipv4_net =         1;   
  ipv6_net =         2;   
  ipv4_connection =  3;   
  ipv6_connection =  4;   
}


enum Update-Targets { 
  file =  1;   
}


enum Delete-Targets { 
  slpf/rule_number =  1;   
}


struct AP-Target { 
  1:  optional  Rule-ID  rule_number;   
}


struct AP-Specifiers { 
  1:  optional  string                     hostname;      
  2:  optional  string                     named_group;   
  3:  optional  string                     asset_id;      
  4:  optional  Ap-specifiers$Asset_tuple  asset_tuple;   
}


struct AP-Args { 
  1:  optional  Drop-Process  drop_process;   
  2:  optional  bool          persistent;     
  3:  optional  Direction     direction;      
  4:  optional  Rule-ID       insert_rule;    
}


struct AP-Results { 
  1:  optional  Rule-ID  rule_number;   
}


enum Drop-Process { 
  none =       1;   
  reject =     2;   
  false_ack =  3;   
}


enum Direction { 
  both =     1;   
  ingress =  2;   
  egress =   3;   
}

// Rule-ID(Integer)

enum Status-Code { 
  Processing =           102;   
  OK =                   200;   
  Created =              201;   
  Bad_Request =          400;   
  Unauthorized =         401;   
  Forbidden =            403;   
  Not_Found =            404;   
  Internal_Error =       500;   
  Not_Implemented =      501;   
  Service_Unavailable =  503;   
}


struct Features {
  1: optional list<string> item; 
}


struct File { 
  1:  optional  string  name;     
  2:  optional  string  path;     
  3:  optional  Hashes  hashes;   
}


struct IPv4-Net {
  1: optional list<string> item; 
}


struct IPv4-Connection { 
  1:  optional  IPv4-Net     src_addr;   
  2:  optional  Port         src_port;   
  3:  optional  IPv4-Net     dst_addr;   
  4:  optional  Port         dst_port;   
  5:  optional  L4-Protocol  protocol;   
}


struct IPv6-Net {
  1: optional list<string> item; 
}


struct IPv6-Connection { 
  1:  optional  IPv6-Net     src_addr;   
  2:  optional  Port         src_port;   
  3:  optional  IPv6-Net     dst_addr;   
  4:  optional  Port         dst_port;   
  5:  optional  L4-Protocol  protocol;   
}

// Date-Time(Integer)
// Duration(Integer)

enum Feature { 
  versions =    1;   
  profiles =    2;   
  pairs =       3;   
  rate_limit =  4;   
  args =        5;   
}


struct Hashes { 
  1:  optional  Hashes$md5     md5;      
  2:  optional  Hashes$sha1    sha1;     
  3:  optional  Hashes$sha256  sha256;   
}

// IPv4-Addr(Binary)
// IPv6-Addr(Binary)

enum L4-Protocol { 
  icmp =  1;     
  tcp =   6;     
  udp =   17;    
  sctp =  132;   
}

// Port(Integer)

enum Response-Type { 
  none =      0;   
  ack =       1;   
  status =    2;   
  complete =  3;   
}

// Version(String)
// Namespace(String)
// Command-ID(String)

struct Results$Versions {
  1: optional list<string> item; 
}


struct Results$Profiles {
  1: optional list<string> item; 
}


struct Results$Args {
  1: optional list<string> item; 
}


struct Action-targets$Query {
  1: optional list<string> item; 
}


struct Action-targets$Deny {
  1: optional list<string> item; 
}


struct Action-targets$Allow {
  1: optional list<string> item; 
}


struct Action-targets$Update {
  1: optional list<string> item; 
}


struct Action-targets$Delete {
  1: optional list<string> item; 
}


struct Ap-specifiers$Asset_tuple {
  1: optional list<string> item; 
}

// Results$rate-limit(Number)
// Hashes$md5(Binary)
// Hashes$sha1(Binary)
// Hashes$sha256(Binary)
