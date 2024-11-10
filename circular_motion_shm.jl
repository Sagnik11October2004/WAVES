using Plots

# Function to calculate particle position in the circle
function circular_motion(t, radius=1.0)
    x = radius * cos(t)
    y = radius * sin(t)
    return x, y
end

# Parameters for simulation
radius = 1.0
T = 2π  # Time for one full cycle (2π for one rotation)
dt = 0.05  # Time step
t_vals = 0:dt:T  # Time vector

# Create a GIF to store the animation
anim = @animate for t in t_vals
    x, y = circular_motion(t, radius)
    
    # Create the circular motion plot
    p1 = plot([x], [y], seriestype=:scatter, label="Particle", 
              xlabel="x", ylabel="y", 
              xlims=(-1.5, 1.5), ylims=(-1.5, 1.5),
              title="Circular Motion", aspect_ratio=:equal)
    # Add the circle path
    plot!([radius*cos(theta) for theta in 0:0.1:2π], 
          [radius*sin(theta) for theta in 0:0.1:2π], 
          label="Path", color=:blue)

    # Create the projection plot
    p2 = plot(t_vals, [circular_motion(t, radius)[1] for t in t_vals], 
              label="Projection on x-axis", 
              xlabel="Time", ylabel="x",
              xlims=(0, T), ylims=(-1.5, 1.5), 
              title="X-Projection")
    scatter!(p2, [t], [x], label="Current Projection", color=:red)

    # Create a combined plot
    plot(p1, p2, layout=@layout [a; b])
end

# Save the animation as a GIF
gif(anim, "circular_motion_animation.gif", fps=15)