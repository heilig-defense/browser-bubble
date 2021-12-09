<Serializable()>
Public Class STATE
    Public License As Integer = 0
    Public Drivers As Integer = 0
    Public Browsers As Integer = 0
    Public Options As Integer = 0
    Public InitErrors As New Dictionary(Of Integer, String)
    Public Update As Integer = 0
    Public UpdateVersion As String = String.Empty
    Public UpdateMessage As String = String.Empty
    Public SavedBubbles As Integer = 0
    Public RunningBubbles As Integer = 0
End Class
