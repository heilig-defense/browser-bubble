using System;

[Serializable()]
public partial class SERVER_RESPONSE
{
    public int ErrorCode = 0;
    public int DataType = 0;
    public int Version = 1;
    public long MessageID = 0L;
    public string ReturnValue = string.Empty;
}