using System;

[Serializable()]
public partial class PROXY_SERVER
{
    public long ID = 0L;
    public string ProxyName = string.Empty;
    public COUNTRY Country = new COUNTRY();
    public string IP = string.Empty;
    public int Port = 0;
    public int ProxyType = 0;
    public int Flags = 0;
}