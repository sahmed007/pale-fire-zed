defmodule ThemePreview.Counter do
  @moduledoc """
  A small counter for comparing modules, atoms, strings, and numbers.
  """

  @limit 42
  defstruct name: "ready", value: 0, enabled: true

  @type t :: %__MODULE__{name: String.t(), value: integer(), enabled: boolean()}

  @doc "Advance a counter by a non-negative step."
  @spec advance(t(), integer()) :: {:ok, t()} | {:error, atom()}
  def advance(%__MODULE__{enabled: false}, _step), do: {:error, :disabled}

  def advance(%__MODULE__{value: value} = counter, step)
      when is_integer(step) and step >= 0 do
    if value + step <= @limit do
      {:ok, %{counter | value: value + step}}
    else
      {:error, :limit_reached}
    end
  end

  def advance(_counter, _step), do: {:error, :invalid_step}

  def demo do
    # Pipelines, anonymous functions, captures, and pattern matching.
    steps = [1, 2, 42] |> Enum.filter(&(&1 > 0))

    Enum.each(steps, fn step ->
      case advance(%__MODULE__{}, step) do
        {:ok, %{name: name, value: value}} ->
          IO.puts("#{name}: #{value}\n")

        {:error, reason} ->
          IO.inspect(reason, label: "counter error")
      end
    end)

    labels = ~w(ready waiting empty)
    for label <- labels, String.match?(label, ~r/^r\w+$/i), do: String.upcase(label)
  end
end

ThemePreview.Counter.demo() |> IO.inspect(label: "matching labels")
