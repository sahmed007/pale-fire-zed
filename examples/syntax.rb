module Sample
  # Symbols, strings, constants, methods, and instance variables.
  class Counter
    LIMIT = 42

    def initialize(step: 2)
      @step = step
    end

    def call(values)
      values.each do |value|
        next if value.nil?

        return { status: :ready, message: "value: #{value}\n" } if value > LIMIT
      end
      { status: :waiting, step: @step }
    rescue ArgumentError => error
      warn error.message
    end
  end
end
