Imports System

Module Program
    Private Structure instruction
        Public opcode As String
        Public operand As Integer
        Public count As UInteger
    End Structure

    Sub Main(args As String())
        Dim currentRow As String()
        Dim opsList As New List(Of instruction)

        Using MyReader As New Microsoft.VisualBasic.FileIO.TextFieldParser("input")
            MyReader.TextFieldType = FileIO.FieldType.Delimited
            MyReader.SetDelimiters(" ")
            While Not MyReader.EndOfData
                currentRow = MyReader.ReadFields()
                If currentRow.Length = 2 Then
                    Dim op As instruction
                    op.opcode = currentRow.ElementAt(0)
                    op.operand = Integer.Parse(currentRow.ElementAt(1))
                    opsList.Add(op)
                End If
            End While
        End Using

        Dim ops = opsList.ToArray()
        Dim pc As Integer
        Dim acc As Integer
        pc = 0
        acc = 0

        While True

            Dim op As instruction

            If pc >= ops.Count() Or pc < 0 Then
                Console.WriteLine("invalid memory address " & pc)
                Return
            End If

            op = ops.ElementAt(pc)
            op.count = op.count + 1
            ops.SetValue(op, pc)

            If op.count > 1 Then
                Console.WriteLine("Revisited instruction " & op.opcode & " " & op.operand & " at " & pc & " with acc = " & acc)
                Return
            End If
            Select Case op.opcode
                Case "nop"
                    pc = pc + 1
                Case "acc"
                    acc = acc + op.operand
                    pc = pc + 1
                Case "jmp"
                    pc = pc + op.operand
                Case Else
                    Console.WriteLine("invalid instruction " & op.operand & " at " & pc)
                    Return
            End Select
        End While



    End Sub
End Module
