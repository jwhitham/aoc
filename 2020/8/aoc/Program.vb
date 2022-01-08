Imports System

Module Program
    Private Structure instruction
        Public opcode As String
        Public operand As Integer
        Public count As UInteger
    End Structure

    Const ErrorValue = Integer.MinValue

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

        Console.WriteLine("Part 1 - unmodified program")
        Dim acc = Test(opsList.ToArray(), True)
        If acc = ErrorValue Then
            Console.WriteLine("Program did not loop")
        Else
            Console.WriteLine("Program looped with acc = " & acc)
        End If
        Console.WriteLine("Part 2 - try to fix")
        For i As Integer = 0 To opsList.Count() - 1
            Dim ops = opsList.ToArray()
            Dim op = ops.ElementAt(i)
            Dim backup = op
            Dim skip = False
            Select Case op.opcode
                Case "nop"
                    op.opcode = "jmp"
                Case "jmp"
                    op.opcode = "nop"
                Case Else
                    skip = True
            End Select
            If Not skip Then
                ops.SetValue(op, i)
                acc = Test(ops, False)
                If acc <> ErrorValue Then
                    Console.WriteLine("Program is fixed with modification at index " & i & " acc = " & acc)
                    Return
                End If
                ops.SetValue(backup, i)
            End If
        Next
        Console.WriteLine("Program cannot be fixed")
    End Sub
    Private Function Test(ops As instruction(), expectLoop As Boolean) As Integer
        Dim pc As Integer
        Dim acc As Integer
        pc = 0
        acc = 0

        While True

            Dim op As instruction

            If pc > ops.Count() Or pc < 0 Then
                REM Console.WriteLine("invalid memory address " & pc)
                Return ErrorValue
            End If
            If pc = ops.Count() Then
                REM Console.WriteLine("program completed at " & pc)
                If expectLoop Then
                    Return ErrorValue
                Else
                    Return acc
                End If
            End If

            op = ops.ElementAt(pc)
            op.count = op.count + 1
            ops.SetValue(op, pc)

            If op.count > 1 Then
                REM Console.WriteLine("Revisited instruction " & op.opcode & " " & op.operand & " at " & pc & " with acc = " & acc)
                If expectLoop Then
                    Return acc
                Else
                    Return ErrorValue
                End If
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
                    REM Console.WriteLine("invalid instruction " & op.operand & " at " & pc)
                    Return ErrorValue
            End Select
        End While



    End Function
End Module
