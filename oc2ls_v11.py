from jadnschema.schema import Schema
from jadnschema.schema.info import Information
from jadnschema.schema.definitions import *


# Primitive Types
DomainName = String  # ["/hostname"], "[RFC1034], Section 3.5", []],
EmailAddr = String  # ["/email"], "Email address - [RFC5322], Section 3.4.1", []],
IDNDomainName = String  # ["/idn-hostname"], "Internationalized Domain Name - [RFC5890], Section 2.3.2.3", []],
IDNEmailAddr = String  # ["/idn-email"], "Internationalized email address - [RFC6531]", []],
IRI = String  # ["/iri"], "Internationalized Resource Identifier, [RFC3987]", []],
MACAddr = Binary  # ["/eui"], "Media Access Control / Extended Unique Identifier address - EUI-48 or EUI-64 as defined in [EUI]", []],
URI = String  # ["/uri"], "Uniform Resource Identifier, [RFC3986]", []],
DateTime = Integer  # ["{0"], "Date and Time", []],
Duration = Integer  # ["{0"], "A length of time", []],
Hostname = String  # ["/hostname"], "Internet host name as specified in [RFC1123]", []],
IDNHostname = String  # ["/idn-hostname"], "Internationalized Internet host name as specified in [RFC5890], Section 2.3.2.3", []],
IPv4Addr = Binary  # ["/ipv4-addr"], "32 bit IPv4 address as defined in [RFC0791]", []],
IPv6Addr = Binary  # ["/ipv6-addr"], "128 bit IPv6 address as defined in [RFC8200]", []],
Port = Integer  # ["{0", "}65535"], "Transport Protocol Port Number, [RFC6335]", []],
Version = String  # [], "Major.Minor version number", []],
Namespace = String  # ["/uri"], "Unique name of an Actuator Profile", []],
CommandID = String  # ["%^\\S{0,36}$"], "Command Identifier", []]


# Shared
class Payload(Choice):
    bin: Binary  # 1, [], "Specifies the data contained in the artifact"],
    url: URI  # 2, [], "MUST be a valid URL that resolves to the un-encoded content"]


class L4Protocol(Enumerated):
    """
    Value of the protocol (IPv4) or next header (IPv6) field in an IP packet. Any IANA value, [RFC5237]
    """
    icmp = "icmp"  # 1, "Internet Control Message Protocol - [RFC0792]"],
    tcp = "tcp"  # 6, "Transmission Control Protocol - [RFC0793]"],
    udp = "udp"  # 17, "User Datagram Protocol - [RFC0768]"],
    sctp = "sctp"  # 132, "Stream Control Transmission Protocol - [RFC4960]"]


class Hashes(Map):
    """
    Cryptographic hash values
    """
    md5: Binary  # 1, ["/x", "{16", "}16"], "MD5 hash as defined in [RFC1321]"],
    sha1: Binary  # 2, ["/x", "{20", "}20"], "SHA1 hash as defined in [RFC6234]"],
    sha256: Binary  # 3, ["/x", "{32", "}32"], "SHA256 hash as defined in [RFC6234]"]

    class Options:
        minProperties = 1


class Properties(ArrayOf):
    """
    A list of names that uniquely identify properties of an Actuator"
    """
    class Options:
        valueType = String
        minProperties = 1
        unique = 1


class File(Map):
    name: String  # 1, ["[0"], "The name of the file as defined in the file system"],
    path: String  # 2, ["[0"], "The absolute path to the location of the file in the file system"],
    hashes: Hashes  # 3, ["[0"], "One or more cryptographic hash codes of the file contents"]

    class Options:
        minProperties = 1


class Process(Map):
    pid: Integer  # 1, ["{0", "[0"], "Process ID of the process"],
    name: String  # 2, ["[0"], "Name of the process"],
    cwd: String  # 3, ["[0"], "Current working directory of the process"],
    executable: File  # 4, ["[0"], "Executable that was executed to start the process"],
    parent: 'Process'  # 5, ["[0"], "Process that spawned this one"],
    command_line: String  # 6, ["[0"], "The full command line invocation used to start this process, including all arguments"]

    class Options:
        minProperties = 1


class IPv4Net(Array):
    """
    IPv4 address and prefix length
    """
    ipv4_addr: IPv4Addr  # 1, [], "IPv4 address as defined in [RFC0791]"],
    prefix_length: Integer  # 2, ["[0"], "CIDR prefix-length. If omitted, refers to a single host address"]

    class Options:
        # ["/ipv4-net"]
        pass


class IPv4Connection(Record):
    """
    5-tuple that specifies a tcp/ip connection
    """
    src_addr: IPv4Net  # 1, ["[0"], "IPv4 source address range"],
    src_port: Port  # 2, ["[0"], "Source service per [RFC6335]"],
    dst_addr: IPv4Net  # 3, ["[0"], "IPv4 destination address range"],
    dst_port: Port  # 4, ["[0"], "Destination service per [RFC6335]"],
    protocol: L4Protocol  # 5, ["[0"], "Layer 4 protocol (e.g., TCP) - see L4-Protocol section"]

    class Options:
        minProperties = 1


class IPv6Net(Array):
    """
    IPv4 address and prefix length
    """
    ipv4_addr: IPv6Addr  # 1, [], "IPv4 address as defined in [RFC0791]"],
    prefix_length: Integer  # 2, ["[0"], "CIDR prefix-length. If omitted, refers to a single host address"]

    class Options:
        # ["/ipv4-net"]
        pass


class IPv6Connection(Record):
    """
    5-tuple that specifies a tcp/ip connection
    """
    src_addr: IPv6Net  # 1, ["[0"], "IPv4 source address range"],
    src_port: Port  # 2, ["[0"], "Source service per [RFC6335]"],
    dst_addr: IPv6Net  # 3, ["[0"], "IPv4 destination address range"],
    dst_port: Port  # 4, ["[0"], "Destination service per [RFC6335]"],
    protocol: L4Protocol  # 5, ["[0"], "Layer 4 protocol (e.g., TCP) - see L4-Protocol section"]

    class Options:
        minProperties = 1

class Feature(Enumerated):
    """
    Specifies the results to be returned from a query features Command
    """
    versions = "versions"  # 1, "List of OpenC2 Language versions supported by this Actuator"],
    profiles = "profiles"  # 2, "List of profiles supported by this Actuator"],
    pairs = "pairs"  # 3, "List of supported Actions and applicable Targets"],
    rate_limit = "rate_limit"  # 4, "Maximum number of Commands per minute supported by design or policy"],
    args = "args"  # 5, "List of supported Command Argumemnts"]


class Features(ArrayOf):
    """
    An array of zero to ten names used to query an Actuator for its supported capabilities
    """
    class Options:
        valuesType = Feature
        maxProperties = 10
        unique = True


class Device(Map):
    hostname: Hostname  # 1, ["[0"], "A hostname that can be used to connect to this device over a network"],
    idn_hostname: IDNHostname  # 2, ["[0"], "An internationalized hostname that can be used to connect to this device over a network"],
    device_id: String  # 3, ["[0"], "An identifier that refers to this device within an inventory or management system"]

    class Options:
        minProperties = 1


class Artifact(Record):
    mime_type: String  # 1, ["[0"], "Permitted values specified in the IANA Media Types registry, [RFC6838]"],
    payload: Payload  # 2, ["[0"], "Choice of literal content or URL"],
    hashes: Hashes  # 3, ["[0"], "Hashes of the payload content"]

    class Options:
        minProperties = 1


class Target(Choice):
    artifact: Artifact  # 1, [], "An array of bytes representing a file-like object or a link to that object"
    command: CommandID  # 2, [], "A reference to a previously issued Command"
    device: Device  # 3, [], "The properties of a hardware device"
    domain_name: DomainName  # 7, [], "A network domain name"
    email_addr: EmailAddr  # 8, [], "A single email address"
    features: Features  # 9, [], "A set of items used with the query Action to determine an Actuator's capabilities"
    file: File  # 10, [], "Properties of a file"
    idn_domain_name: IDNDomainName  # 11, [], "An internationalized domain name"
    idn_email_addr: IDNEmailAddr  # 12, [], "A single internationalized email address"
    ipv4_net: IPv4Net  # 13, [], "An IPv4 address range including CIDR prefix length"
    ipv6_net: IPv6Net  # 14, [], "An IPv6 address range including prefix length"
    ipv4_connection: IPv4Connection  # 15, [], "A 5-tuple of source and destination IPv4 address ranges, source and destination ports, and protocol"
    ipv6_connection: IPv6Connection  # 16, [], "A 5-tuple of source and destination IPv6 address ranges, source and destination ports, and protocol"
    iri: IRI  # 20, [], "An internationalized resource identifier (IRI)"
    mac_addr: MACAddr  # 17, [], "A Media Access Control (MAC) address - EUI-48 or EUI-64 as defined in [EUI]"
    process: Process  # 18, [], "Common properties of an instance of a computer program as executed on an operating system"
    properties: Properties  # 25, [], "Data attribute associated with an Actuator"
    uri: URI  # 19, [], "A uniform resource identifier (URI)"


class Action(Enumerated):
    scan = "scan"  # 1, "Systematic examination of some aspect of the entity or its environment"
    locate = "locate"  # 2, "Find an object physically, logically, functionally, or by organization"
    query = "query"  # 3, "Initiate a request for information"
    deny = "deny"  # 6, "Prevent a certain event or action from completion, such as preventing a flow from reaching a destination or preventing access"
    contain = "contain"  # 7, "Isolate a file, process, or entity so that it cannot modify or access assets or processes"
    allow = "allow"  # 8, "Permit access to or execution of a Target"
    start = "start"  # 9, "Initiate a process, application, system, or activity"
    stop = "stop"  # 10, "Halt a system or end an activity"
    restart = "restart"  # 11, "Stop then start a system or an activity"
    cancel = "cancel"  # 14, "Invalidate a previously issued Action"
    set = "set"  # 15, "Change a value, configuration, or state of a managed entity"
    update = "update"  # 16, "Instruct a component to retrieve, install, process, and operate in accordance with a software update, reconfiguration, or other update"
    redirect = "redirect"  # 18, "Change the flow of traffic to a destination other than its original destination"
    create = "create"  # 19, "Add a new entity of a known type (e.g., data, files, directories)"
    delete = "delete"  # 20, "Remove an entity (e.g., data, files, flows)"
    detonate = "detonate"  # 22, "Execute and observe the behavior of a Target (e.g., file, hyperlink) in an isolated environment"
    restore = "restore"  # 23, "Return a system to a previously known state"
    copy = "copy"  # 28, "Duplicate an object, file, data flow, or artifact"
    investigate = "investigate"  # 30, "Task the recipient to aggregate and report information as it pertains to a security event or incident"
    remediate = "remediate"  # 32, "Task the recipient to eliminate a vulnerability or attack point"


# Response
class ResponseType(Enumerated):
    none = "none"  # 0, "No response"],
    ack = "ack"  # 1, "Respond when Command received"],
    status = "status"  # 2, "Respond with progress toward Command completion"],
    complete = "complete"  # 3, "Respond when all aspects of Command completed"]


class StatusCode(Enumerated):
    processing = "Processing"  # 102, "an interim Response used to inform the Producer that the Consumer has accepted the Command but has not yet completed it"
    ok = "OK" # 200, "the Command has succeeded"
    created = "Created" # 201, "the Command has succeeded and a new resource has been created as a result of it"
    badRequest = "Bad Request"  # 400, "the Consumer cannot process the Command due to something that is perceived to be a Producer error (e.g., malformed Command syntax)"
    unauthorized = "Unauthorized" # 401, "the Command Message lacks valid authentication credentials for the target resource or authorization has been refused for the submitted credentials"
    forbidden = "Forbidden" # 403, "the Consumer understood the Command but refuses to authorize it"
    notFound = "Not Found" # 404, "the Consumer has not found anything matching the Command"
    internalError = "Internal Error" # 500, "the Consumer encountered an unexpected condition that prevented it from performing the Command"
    notImplemented = "Not Implemented" # 501, "the Consumer does not support the functionality required to perform the Command"
    serviceUnavailable = "Service Unavailable" # 503, "the Consumer is currently unable to perform the Command due to a temporary overloading or maintenance of the Consumer"

    class Options:
        id = True


class Targets(ArrayOf):
    """
    List of Target types
    """
    class Options:
        # valueType = >Target
        minProperties = 1
        maxProperties = 0
        unique = True


class ActionTargets(MapOf):
    """
    Map of each action supported by this actuator to the list of targets applicable to that action
    """
    class Options:
        keyType = Action
        valueType = Targets
        minProperties = 1


class Results(Map):
    """
    Response Results
    """
    versions: Version  # 1, ["q", "[0", "]10"], "List of OpenC2 language versions supported by this Actuator"],
    profiles: Namespace  # 2, ["q", "[0", "]0"], "List of profiles supported by this Actuator"],
    pairs: ActionTargets  # 3, ["[0"], "List of targets applicable to each supported Action"],
    rate_limit: Number  # 4, ["y0.0", "[0"], "Maximum number of requests per minute supported by design or policy"],
    args: Enumerated  # 5, ["#Args", "[0", "]0"], "List of supported Command Arguments"]

    class Options:
        minProperties = 1


class OpenC2Response(Record):
    status: StatusCode  # 1, [], "An integer status code"
    status_text: String  # 2, ["[0"], "A free-form human-readable description of the Response status"
    results: Results  # 3, ["[0"], "Map of key:value pairs that contain additional results based on the invoking Command"

    class Options:
        name = "OpenC2-Record"


# Command
class Args(Map):
    start_time: DateTime  # 1, ["[0"], "The specific date/time to initiate the Command"
    stop_time: DateTime  # 2, ["[0"], "The specific date/time to terminate the Command"
    duration: Duration  # 3, ["[0"], "The length of time for an Command to be in effect"
    response_requested: ResponseType  # 4, ["[0"], "The type of Response required for the Command: none, ack, status, complete"

    class Options:
        minProperties = 1


class Actuator(Map):
    actuator: String  # 1, [], ""

    class Options:
        minProperties = 1


class OpenC2Command(Record):
    """
    The Command defines an Action to be performed on a Target
    """
    action: Action  # 1, [], "The task or activity to be performed (i.e., the 'verb')"
    target: Target  # 2, [], "The object of the Action. The Action is performed on the Target"
    args: Args  # 3, ["[0"], "Additional information that applies to the Command"
    actuator: Actuator  # 4, ["[0"], "The subject of the Action. The Actuator executes the Action on the Target"
    command_id: CommandID  # 5, ["[0"], "An identifier of this Command

    class Options:
        name = "OpenC2-Command"


# Root Schema
class OpenC2LangV11(Schema):
    info = Information(
        package="http://oasis-open.org/openc2/oc2ls/v1.1",
        title="OpenC2 Language Profile",
        description="Language Profile from the OpenC2 Language Specification version 1.1",
        exports=["OpenC2-Command", "OpenC2-Response"]
    )
    types = {d.name: d for d in [
        OpenC2Command,
        OpenC2Response,
        Action,
        Target,
        Actuator,
        Args,
        Results,
        ActionTargets,
        Targets,
        StatusCode,
        Artifact,
        Device,
        DomainName,
        EmailAddr,
        Features,
        File,
        IDNDomainName,
        IDNEmailAddr,
        IPv4Net,
        IPv4Connection,
        IPv6Net,
        IPv6Connection,
        IRI,
        MACAddr,
        Process,
        Properties,
        URI,
        DateTime,
        Duration,
        Feature,
        Hashes,
        Hostname,
        IDNHostname,
        IPv4Addr,
        IPv6Addr,
        L4Protocol,
        Payload,
        Port,
        ResponseType,
        Version,
        Namespace,
        CommandID
    ]}
