using System;

[Serializable()]
public partial class DNS_SERVER
{
    public long ProviderID = 0L;
    public string Provider = string.Empty;
    public long ServerID = 0L;
    public string Country = string.Empty;
    public int DNSType = 0;
    public string Address = string.Empty;
    public int Port = 0;
}
