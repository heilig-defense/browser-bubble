using System;

[Serializable()]
public partial class LOG_MESSAGE
{
    public int ErrorCode = 0;
    public int Level = 0;
    public string Location = string.Empty;
    public string Message = string.Empty;
}