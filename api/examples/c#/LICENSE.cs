using System;

[Serializable()]
public partial class LICENSE
{
    public string LicenseKey = string.Empty;
    public int Status = 0;
    public string Expires = string.Empty;
    public long Entitlements = 0L;
    public long EndpointCount = 0L;
}