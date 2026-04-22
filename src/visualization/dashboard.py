import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from collections import deque

# Reuse existing utility functions
from src.utils.reachability_check import manhattan_distance, can_all_robot_reach_target
from src.utils.read_write_csv import extract_robots, extract_target, extract_battery_capacity, extract_chargers


def find_shortest_path(grid_rows, grid_cols, start, end):
    """Find shortest path using BFS (only horizontal/vertical moves)"""
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    
    queue = deque([(start, [start])])
    visited = set([start])
    
    while queue:
        (x, y), path = queue.popleft()
        
        if (x, y) == end:
            return path
        
        for dx, dy in directions:
            nx_pos, ny_pos = x + dx, y + dy
            if 0 <= nx_pos < grid_rows and 0 <= ny_pos < grid_cols:
                new_pos = (nx_pos, ny_pos)
                if new_pos not in visited:
                    visited.add(new_pos)
                    queue.append((new_pos, path + [new_pos]))
    
    return None


def find_path_to_target(start, target, stations, capacity, grid_rows, grid_cols):
    """Find path from robot to target using stations if needed"""
    path = find_shortest_path(grid_rows, grid_cols, start, target)
    if path and len(path) - 1 <= capacity:
        return path, []

    best_path = None
    best_stations_used = []
    
    for station in stations:
        path_to_station = find_shortest_path(grid_rows, grid_cols, start, station)
        if path_to_station and len(path_to_station) - 1 <= capacity:
            path_from_station = find_shortest_path(grid_rows, grid_cols, station, target)
            if path_from_station and len(path_from_station) - 1 <= capacity:
                combined_path = path_to_station + path_from_station[1:]
                if best_path is None or len(combined_path) < len(best_path):
                    best_path = combined_path
                    best_stations_used = [station]
    
    if best_path:
        return best_path, best_stations_used

    # Multi-station path finding
    queue = deque([(start, [start], [])])
    visited = {start: 0}
    
    while queue:
        current_pos, path, stations_used = queue.popleft()
        
        path_to_target = find_shortest_path(grid_rows, grid_cols, current_pos, target)
        if path_to_target and len(path_to_target) - 1 <= capacity:
            final_path = path + path_to_target[1:]
            return final_path, stations_used
        
        for station in stations:
            if station not in stations_used:
                path_to_station = find_shortest_path(grid_rows, grid_cols, current_pos, station)
                if path_to_station and len(path_to_station) - 1 <= capacity:
                    new_path = path + path_to_station[1:]
                    new_stations = stations_used + [station]
                    
                    if station not in visited or len(new_path) < visited[station]:
                        visited[station] = len(new_path)
                        queue.append((station, new_path, new_stations))
    
    return None, []


def visualize_data_summary(df, grid_rows, grid_cols):
    st.header("📊 Data Summary")
    
    total_rows = len(df)
    total_robots = 0
    failed_rows = 0
    failed_details = []
    robot_counts = []
    capacity_stats = []
    
    for index, row in df.iterrows():
        robots = extract_robots(row)
        stations = extract_chargers(row)
        target = extract_target(row)
        capacity = extract_battery_capacity(row)
        
        robot_counts.append(len(robots))
        total_robots += len(robots)
        capacity_stats.append(capacity)
        
        # Use existing reachability check
        from src.utils.reachability_check import reachable_robots
        reached_robots_set = reachable_robots(target, robots, stations, capacity)
        
        if len(reached_robots_set) != len(robots):
            failed_rows += 1
            failed_details.append({
                'Row': index + 1,
                'Total Robots': len(robots),
                'Reached Robots': len(reached_robots_set),
                'Failed Robots': len(robots) - len(reached_robots_set)
            })
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Rows", total_rows)
    with col2:
        st.metric("Total Robots", total_robots)
    with col3:
        st.metric("Failed Rows", failed_rows)
    with col4:
        success_rate = ((total_rows - failed_rows) / total_rows * 100) if total_rows > 0 else 0
        st.metric("Success Rate", f"{success_rate:.1f}%")
    
    col1, col2 = st.columns(2)
    
    with col1:
        robot_count_df = pd.DataFrame({'Robot Count': robot_counts})
        count_summary = robot_count_df['Robot Count'].value_counts().sort_index()
        
        fig1 = go.Figure()
        fig1.add_trace(go.Bar(
            x=count_summary.index,
            y=count_summary.values,
            marker=dict(
                color=count_summary.values,
                colorscale='Blues',
                showscale=True,
                colorbar=dict(title="Frequency")
            ),
            text=count_summary.values,
            textposition='outside',
            hovertemplate='<b>%{x} Robots</b><br>Frequency: %{y}<extra></extra>'
        ))
        
        fig1.update_layout(
            title=dict(text="Robot Count Distribution", font=dict(size=16, color='#2c3e50')),
            xaxis=dict(title="Number of Robots per Row", showgrid=True, gridcolor='lightgray', dtick=1),
            yaxis=dict(title="Frequency", showgrid=True, gridcolor='lightgray'),
            plot_bgcolor='rgba(240, 240, 240, 0.5)',
            paper_bgcolor='white',
            hovermode='closest',
            height=400
        )
        
        st.plotly_chart(fig1, use_container_width=True)
        
        st.markdown(f"""
        **Statistics:**
        - **Mean:** {np.mean(robot_counts):.2f} robots
        - **Median:** {np.median(robot_counts):.0f} robots
        - **Range:** {min(robot_counts)} - {max(robot_counts)} robots
        """)
    
    with col2:
        capacity_df = pd.DataFrame({'Capacity': capacity_stats})
        capacity_summary = capacity_df['Capacity'].value_counts().sort_index()
        
        fig2 = go.Figure()
        fig2.add_trace(go.Bar(
            x=capacity_summary.index,
            y=capacity_summary.values,
            marker=dict(
                color=capacity_summary.values,
                colorscale='Greens',
                showscale=True,
                colorbar=dict(title="Frequency")
            ),
            text=capacity_summary.values,
            textposition='outside',
            hovertemplate='<b>Capacity: %{x}</b><br>Frequency: %{y}<extra></extra>'
        ))
        
        fig2.update_layout(
            title=dict(text="Battery Capacity Distribution", font=dict(size=16, color='#2c3e50')),
            xaxis=dict(title="Battery Capacity (units)", showgrid=True, gridcolor='lightgray', dtick=1),
            yaxis=dict(title="Frequency", showgrid=True, gridcolor='lightgray'),
            plot_bgcolor='rgba(240, 240, 240, 0.5)',
            paper_bgcolor='white',
            hovermode='closest',
            height=400
        )
        
        st.plotly_chart(fig2, use_container_width=True)
        
        st.markdown(f"""
        **Statistics:**
        - **Mean:** {np.mean(capacity_stats):.2f} units
        - **Median:** {np.median(capacity_stats):.0f} units
        - **Range:** {min(capacity_stats)} - {max(capacity_stats)} units
        """)
    
    if failed_details:
        st.subheader("❌ Failed Rows Details")
        failed_df = pd.DataFrame(failed_details)
        st.dataframe(failed_df)
    
    return failed_details


def visualize_robot_paths(df, selected_row, grid_rows, grid_cols):
    st.header("🤖 Robot Path Visualization")
    
    row = df.iloc[selected_row]
    
    robots_list = extract_robots(row)
    stations = extract_chargers(row)
    target = extract_target(row)
    capacity = extract_battery_capacity(row)
    
    robots = {}
    for i, pos in enumerate(robots_list, 1):
        robots[f'R{i}'] = pos
    
    robot_positions = list(robots.values())
    
    # Use existing reachability check
    from src.utils.reachability_check import reachable_robots
    reached_robots_set = reachable_robots(target, robot_positions, stations, capacity)
    reached_robots = list(reached_robots_set)
    
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric("Total Robots", len(robots))
    with col2:
        st.metric("Charging Stations", len(stations))
    with col3:
        st.metric("Battery Capacity", capacity)
    with col4:
        st.metric("Reachable", len(reached_robots), delta=f"{len(reached_robots)-len(robots)}")
    with col5:
        st.metric("Grid Size", f"{grid_rows}×{grid_cols}")
    
    fig = go.Figure()
    
    # Grid lines
    for x in range(grid_rows + 1):
        fig.add_shape(type="line", x0=x, y0=0, x1=x, y1=grid_cols, 
                     line=dict(color="rgba(200, 200, 200, 0.3)", width=0.5))
    for y in range(grid_cols + 1):
        fig.add_shape(type="line", x0=0, y0=y, x1=grid_rows, y1=y, 
                     line=dict(color="rgba(200, 200, 200, 0.3)", width=0.5))
    
    # Target range diamond
    def create_diamond_outline(center_x, center_y, radius):
        points_x = [center_x, center_x + radius, center_x, center_x - radius, center_x]
        points_y = [center_y + radius, center_y, center_y - radius, center_y, center_y + radius]
        return points_x, points_y
    
    diamond_x, diamond_y = create_diamond_outline(target[0], target[1], capacity)
    fig.add_trace(go.Scatter(
        x=diamond_x, y=diamond_y, 
        mode='lines',
        line=dict(color='red', width=1, dash='dot'),
        fill='toself',
        fillcolor='rgba(255, 0, 0, 0.03)',
        name=f'Target Range (capacity={capacity})',
        showlegend=True,
        hoverinfo='skip'
    ))
    
    # Station ranges
    for idx, station in enumerate(stations):
        diamond_x, diamond_y = create_diamond_outline(station[0], station[1], capacity)
        fig.add_trace(go.Scatter(
            x=diamond_x, y=diamond_y,
            mode='lines',
            line=dict(color='green', width=1, dash='dot'),
            fill='toself',
            fillcolor='rgba(0, 255, 0, 0.03)',
            name='Station Range' if idx == 0 else '',
            showlegend=(idx == 0),
            legendgroup='station_range',
            hoverinfo='skip'
        ))
    
    colors = ['#9C27B0', '#2196F3', '#4CAF50', '#FF9800', '#00BCD4', '#E91E63', 
              '#8BC34A', '#3F51B5', '#009688', '#F44336', '#CDDC39', '#FF5722']
    
    path_info = []
    stations_used_by_robots = set()
    
    for idx, (robot_name, robot_pos) in enumerate(robots.items()):
        if robot_pos in reached_robots:
            path, stations_used = find_path_to_target(robot_pos, target, stations, capacity, grid_rows, grid_cols)
            if path:
                path_x, path_y = zip(*path)
                color = colors[idx % len(colors)]
                
                for station in stations_used:
                    stations_used_by_robots.add(station)
                
                fig.add_trace(go.Scatter(
                    x=path_x, y=path_y, mode='lines',
                    line=dict(color=color, width=2.5, shape='linear'),
                    name=f'{robot_name}',
                    showlegend=True,
                    hoverinfo='skip'
                ))
                
                path_str = " → ".join([f"({x},{y})" for x, y in path[:3]])
                if len(path) > 3:
                    path_str += f" → ... → ({path[-1][0]},{path[-1][1]})"
                
                path_info.append({
                    'Robot': robot_name,
                    'Start': f"({robot_pos[0]}, {robot_pos[1]})",
                    'End': f"({target[0]}, {target[1]})",
                    'Steps': len(path) - 1,
                    'Stations Used': len(stations_used),
                    'Path Preview': path_str
                })
    
    # Target marker
    fig.add_trace(go.Scatter(
        x=[target[0]], y=[target[1]], mode='markers+text', 
        name='🎯 Target', 
        marker=dict(size=24, color='red', symbol='star',
                   line=dict(color='darkred', width=2)),
        text=["TARGET"],
        textfont=dict(size=8, color='white', family='Arial Black'),
        textposition="middle center",
        hovertemplate='<b>Target</b><br>Position: (%{x}, %{y})<extra></extra>'
    ))
    
    # Stations markers
    if stations:
        station_x, station_y = zip(*stations)
        
        if len(stations) > 10:
            fig.add_trace(go.Scatter(
                x=station_x, y=station_y, mode='markers', 
                name=f'⚡ Stations ({len(stations)})', 
                marker=dict(size=14, color='green', symbol='square', 
                           line=dict(color='darkgreen', width=2)),
                hovertemplate='<b>Station %{customdata}</b><br>Position: (%{x}, %{y})<extra></extra>',
                customdata=[f"S{i+1}" for i in range(len(stations))]
            ))
        else:
            fig.add_trace(go.Scatter(
                x=station_x, y=station_y, mode='markers+text', 
                name=f'⚡ Stations ({len(stations)})', 
                marker=dict(size=14, color='green', symbol='square',
                           line=dict(color='darkgreen', width=2)),
                text=[f"S{i+1}" for i in range(len(stations))],
                textposition="top center",
                textfont=dict(size=9, color='darkgreen', family='Arial Black'),
                hovertemplate='<b>Station %{text}</b><br>Position: (%{x}, %{y})<extra></extra>'
            ))
    
    # Robots markers
    robot_x, robot_y = zip(*robot_positions) if robot_positions else ([], [])
    robot_names = list(robots.keys())
    
    if len(robots) > 15:
        fig.add_trace(go.Scatter(
            x=robot_x, y=robot_y, mode='markers', 
            name=f'🤖 Robots ({len(robots)})', 
            marker=dict(size=12, color='blue', symbol='circle',
                       line=dict(color='darkblue', width=1)),
            hovertemplate='<b>%{customdata}</b><br>Position: (%{x}, %{y})<extra></extra>',
            customdata=robot_names
        ))
    else:
        fig.add_trace(go.Scatter(
            x=robot_x, y=robot_y, mode='markers+text', 
            name=f'🤖 Robots ({len(robots)})', 
            marker=dict(size=12, color='blue', symbol='circle',
                       line=dict(color='darkblue', width=1)),
            text=robot_names,
            textposition="top center",
            textfont=dict(size=8, color='darkblue'),
            hovertemplate='<b>%{text}</b><br>Position: (%{x}, %{y})<extra></extra>'
        ))
    
    # Unreachable robots
    unreachable_robots = [robot_pos for robot_pos in robot_positions if robot_pos not in reached_robots]
    unreachable_names = [name for name, pos in robots.items() if pos not in reached_robots]
    
    if unreachable_robots:
        unreachable_x, unreachable_y = zip(*unreachable_robots)
        if len(unreachable_robots) > 10:
            fig.add_trace(go.Scatter(
                x=unreachable_x, y=unreachable_y, mode='markers', 
                name=f'❌ Unreachable ({len(unreachable_robots)})', 
                marker=dict(size=16, color='black', symbol='x', 
                           line=dict(color='red', width=2)),
                hovertemplate='<b>%{customdata}</b> (Unreachable)<br>Position: (%{x}, %{y})<extra></extra>',
                customdata=unreachable_names
            ))
        else:
            fig.add_trace(go.Scatter(
                x=unreachable_x, y=unreachable_y, mode='markers+text', 
                name=f'❌ Unreachable ({len(unreachable_robots)})', 
                marker=dict(size=16, color='black', symbol='x',
                           line=dict(color='red', width=2)),
                text=unreachable_names,
                textposition="top center",
                textfont=dict(size=8, color='black', family='Arial Black'),
                hovertemplate='<b>%{text}</b> (Unreachable)<br>Position: (%{x}, %{y})<extra></extra>'
            ))
    
    fig.update_layout(
        title=dict(
            text=f"Robot Paths Analysis - Row {selected_row + 1}",
            font=dict(size=18, color='#2c3e50', family='Arial Black')
        ),
        xaxis=dict(
            range=[-0.5, grid_rows + 0.5], 
            title='X Coordinate (Rows)',
            gridcolor='rgba(200, 200, 200, 0.3)',
            showgrid=True,
            zeroline=False
        ),
        yaxis=dict(
            range=[-0.5, grid_cols + 0.5], 
            title='Y Coordinate (Columns)', 
            scaleanchor="x",
            gridcolor='rgba(200, 200, 200, 0.3)',
            showgrid=True,
            zeroline=False
        ),
        showlegend=True,
        legend=dict(
            orientation="v",
            yanchor="top",
            y=1,
            xanchor="left",
            x=1.01,
            bgcolor="rgba(255, 255, 255, 0.95)",
            bordercolor="lightgray",
            borderwidth=1,
            font=dict(size=10)
        ),
        width=950,
        height=750,
        hovermode='closest',
        plot_bgcolor='rgba(250, 250, 250, 0.95)',
        paper_bgcolor='white',
        margin=dict(r=150)
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    if path_info:
        st.subheader("📍 Detailed Path Information")
        path_df = pd.DataFrame(path_info)
        st.dataframe(path_df, use_container_width=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.success(f"**✓ Reachable:** {len(reached_robots)} / {len(robots)}")
    with col2:
        st.error(f"**✗ Unreachable:** {len(unreachable_robots)} / {len(robots)}")
    with col3:
        st.info(f"**🔋 Stations Used:** {len(stations_used_by_robots)} / {len(stations)}")


def run_dashboard():
    """Main function to run the Streamlit dashboard"""
    st.set_page_config(
        page_title="Robot Path Analysis Dashboard",
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    st.title("🤖 Robot Path Analysis Dashboard")
    st.markdown("---")
    
    st.sidebar.header("📁 Data Configuration")
    
    uploaded_file = st.sidebar.file_uploader(
        "Upload CSV File", 
        type=['csv'],
        help="Upload a CSV file with robot positions, stations, target, and capacity"
    )
    
    st.sidebar.header("🗺️ Grid Dimensions")
    
    col1, col2 = st.sidebar.columns(2)
    with col1:
        grid_rows = st.number_input(
            "Number of Rows", 
            min_value=1, 
            max_value=100, 
            value=20,
            help="Number of rows in the grid (Y-axis)"
        )
    with col2:
        grid_cols = st.number_input(
            "Number of Columns", 
            min_value=1, 
            max_value=100, 
            value=20,
            help="Number of columns in the grid (X-axis)"
        )
    
    if uploaded_file is None:
        st.sidebar.info("👆 Upload a CSV file to get started")
        st.info("Please upload a CSV file containing robot positions, charging stations, target coordinates, and battery capacity data.")
        st.markdown("""
        ### Expected CSV Format:
        - **Target_x, Target_y**: Target coordinates
        - **R1_x, R1_y, R2_x, R2_y, ...**: Robot positions
        - **Station_1_x, Station_1_y, ...**: Charging station positions
        - **Capacity**: Battery capacity for all robots
        
        ### Grid Dimensions:
        - **Rows**: Number of rows in the grid (Y-axis)
        - **Columns**: Number of columns in the grid (X-axis)
        """)
        return
    else:
        try:
            df = pd.read_csv(uploaded_file)
            st.sidebar.success("✅ File uploaded successfully!")
        except Exception as e:
            st.error(f"Error reading file: {e}")
            return
    
    tab1, tab2 = st.tabs([
        "📊 Data Summary", 
        "🛣️ Path Visualization"
    ])
    
    with tab1:
        visualize_data_summary(df, grid_rows, grid_cols)
    
    with tab2:
        if len(df) > 0:
            st.sidebar.header("🔧 Visualization Settings")
            selected_row = st.sidebar.selectbox(
                "Select Row to Visualize",
                options=range(len(df)),
                format_func=lambda x: f"Row {x + 1}"
            )
            visualize_robot_paths(df, selected_row, grid_rows, grid_cols)
        else:
            st.warning("No data available for visualization")


if __name__ == "__main__":
    run_dashboard()