using System;

[Serializable()]
public partial class VPN_SERVER
{
    public long ID = 0L;
    public string Provider = string.Empty;
    public COUNTRY Country = new COUNTRY();
    public string Address = string.Empty;
    public string Adapter = string.Empty;
}