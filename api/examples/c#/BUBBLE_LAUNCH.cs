using System;
using System.Collections.Generic;

[Serializable()]
public partial class BUBBLE_LAUNCH
{
    public long ID = 0L;
    public int IsInstance = 0;
    public int Flags = 0;
    public string Password = string.Empty;
    public long DNSID = 0L;
    public List<long> ProxyList = new List<long>();
    public long VPNID = 0L;
}