<Serializable()>
Public Class PROXY_SERVER
    Public ID As Long = 0
    Public ProxyName As String = String.Empty
    Public Country As New COUNTRY
    Public IP As String = String.Empty
    Public Port As Integer = 0
    Public ProxyType As Integer = 0
    Public Flags As Integer = 0
End Class
