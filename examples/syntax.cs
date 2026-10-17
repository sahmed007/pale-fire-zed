using System;
using System.Collections.Generic;

namespace ThemePreview;

// Records, nullable types, interpolation, and pattern matching.
public record Item(string Name, int Count);

public static class Preview
{
    public static T? First<T>(IEnumerable<T> values) where T : class
    {
        foreach (var value in values)
        {
            if (value is not null) return value;
        }
        return null;
    }

    public static void Main()
    {
        var item = new Item("ready", 42);
        var status = item.Count switch
        {
            0 => "empty",
            > 10 => "busy",
            _ => "waiting"
        };
        Console.WriteLine($"{item.Name}: {status} ({item.Count})");
    }
}
