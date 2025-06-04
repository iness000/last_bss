import { Bar } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ChartData,
} from 'chart.js';
import { useMemo } from 'react';
import { SwapActivity, Station } from '../../context/DashboardContext';

// Register ChartJS components
ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
);

type SwapStatusChartProps = {
  activities: SwapActivity[];
  stations: Station[];
};

const SwapStatusChart = ({ activities, stations }: SwapStatusChartProps) => {
  // Create a map of station IDs to names for quick lookup
  const stationMap = useMemo(() => {
    const map = new Map<number, string>();
    stations.forEach(station => {
      map.set(station.id, station.name);
    });
    return map;
  }, [stations]);

  // Process the data to get swaps per station for the last 7 days
  const chartData = useMemo(() => {
    // Get the date 7 days ago
    const sevenDaysAgo = new Date();
    sevenDaysAgo.setDate(sevenDaysAgo.getDate() - 7);
    
    // Filter swaps from the last 7 days
    const recentSwaps = activities.filter(swap => {
      const swapDate = new Date(swap.created_at);
      return swapDate >= sevenDaysAgo;
    });
    
 

    // Count swaps per station
    const swapsByStation = new Map<number, number>();
    
    recentSwaps.forEach(swap => {
      const stationId = swap.pickup_station_id;
      const count = swapsByStation.get(stationId) || 0;
      swapsByStation.set(stationId, count + 1);
    });

    // Ensure all stations are represented, even with zero swaps
    stations.forEach(station => {
      if (!swapsByStation.has(station.id)) {
        swapsByStation.set(station.id, 0);
      }
    });

    // Convert to array of { stationName, count } and sort by count (descending)
    const result = Array.from(swapsByStation.entries())
      .map(([stationId, count]) => ({
        stationName: stationMap.get(stationId) || `Station ${stationId}`,
        count,
      }))
      .sort((a, b) => b.count - a.count); // Sort by count descending

    return result;
  }, [activities, stationMap]);

  // Prepare data for Chart.js
  const chartConfig: ChartData<'bar'> = {
    labels: chartData.map(item => item.stationName),
    datasets: [
      {
        label: 'Number of Swaps',
        data: chartData.map(item => item.count),
        backgroundColor: 'rgba(79, 70, 229, 0.8)',
        borderColor: 'rgba(79, 70, 229, 1)',
        borderWidth: 1,
      },
    ],
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'top' as const,
      },
      title: {
        display: true,
        text: 'Swaps per Station (Last 7 Days)',
      },
    },
    scales: {
      y: {
        beginAtZero: true,
        title: {
          display: true,
          text: 'Number of Swaps',
        },
        ticks: {
          stepSize: 1,
          precision: 0,
        },
      },
      x: {
        title: {
          display: true,
          text: 'Station',
        },
      },
    },
  };

  return (
    <div className="bg-white p-6 rounded-xl shadow-soft h-full">
      <div className="h-80">
        <Bar data={chartConfig} options={options} />
      </div>
    </div>
  );
};

export default SwapStatusChart;
