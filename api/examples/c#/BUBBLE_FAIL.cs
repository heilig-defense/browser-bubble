using System;

[Serializable()]
public partial class BUBBLE_FAIL
{
    public long InstanceID = 0L;
    public int ProcessId = 0;
    public string BrowserPath = string.Empty;
    public int ErrorCode = 0;
    public string Log = string.Empty;
}
