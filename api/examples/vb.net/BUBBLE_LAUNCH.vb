<Serializable()>
Public Class BUBBLE_LAUNCH
    Public ID As Long = 0
    Public IsInstance As Integer = 0
    Public Flags As Integer = 0
    Public Password As String = String.Empty
    Public DNSID As Long = 0
    Public ProxyList As New List(Of Long)
    Public VPNID As Long = 0
End Class
