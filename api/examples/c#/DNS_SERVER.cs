using System;

[Serializable()]
public partial class DNS_SERVER
{
    public long ID = 0L;
    public string Provider = string.Empty;
    public string Country = string.Empty;
    public int DNSType = 0;
    public string Address = string.Empty;
    public int Port = 0;
}