using Plots

# Constants
ω₀ = 4.0       # Natural frequency
β = 0.5        # Damping coefficient
F₀ = 1.0       # Amplitude of the driving force
m = 1.0        # Mass of the oscillator
t = 0:0.01:20  # Time array

# Frequencies of the driving force
frequencies = [1.0, 4.0, 7.0]

# Function to calculate position for forced damped oscillator
function forced_damped_oscillator(t, ω, ω₀, β, F₀, m)
    A = 0.0  # Initial amplitude (can be adjusted)
    δ = atan(2 * β * ω / (ω₀^2 - ω^2))  # Phase difference
    return A * exp(-β * t) .* cos.(ω₀ * t) .+ (F₀ / m) * (1 / sqrt((ω₀^2 - ω^2)^2 + (2 * β * ω)^2)) * sin.(ω * t .+ δ)
end

# Create plot
p = plot(t, forced_damped_oscillator.(t, frequencies[1], ω₀, β, F₀, m), label="ω = 1", color=:blue)
plot!(p, t, forced_damped_oscillator.(t, frequencies[2], ω₀, β, F₀, m), label="ω = 4", color=:green)
plot!(p, t, forced_damped_oscillator.(t, frequencies[3], ω₀, β, F₀, m), label="ω = 7", color=:red)

# Customize plot
xlabel!(p, "Time (s)")
ylabel!(p, "Position (x)")
title!(p, "Position-Time Plot of Forced Damped Oscillator")
display(plot!(legend=:topright))
# Save the plot as a PNG file
savefig(p, "forced_damped_oscillator.png")

