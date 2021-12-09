using System;

[Serializable()]
public partial class SERVER_REQUEST
{
    public int Version = 1;
    public long MessageId = 0L;
    public int DataType = 0;
    public string RequestValue = string.Empty;
}