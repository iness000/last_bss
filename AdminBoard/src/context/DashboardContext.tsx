import { createContext, useContext, useState, useEffect } from 'react';


export interface Battery {
  id: number;
  station_id: number | null;
  status: string;
  serial_number: string;
  battery_type: string;
  battery_capacity: number;
  manufacture_date: string;
  created_at: string;
  updated_at: string;
  latest_soh_percent?: number; // Added optional latest_soh_percent
}

export interface Station {
  id: number;
  station_id: string;
  name: string;
  location: {
    lat: number;
    lng: number;
  };
  status: string;
  total_slots: number;
  available_slots: number;
  created_at: string;
  updated_at: string;
}

export interface SwapActivity {
  id: number;
  user_id: number;
  battery_in_id: string;
  battery_out_id: string;
  station_id: number;
  status: string;
  start_time: string;
  end_time: string | null;
  battery_percentage_start: number;
  battery_percentage_end: number;
  ah_used: number;
  created_at: string;
  updated_at: string;
  pickup_station_id: number;
}

interface DashboardContextType {
  batteries: Battery[];
  stations: Station[];
  swapActivities: SwapActivity[];
  users: User[];
}

const DashboardContext = createContext<DashboardContextType | undefined>(undefined);

// Helper to robustly extract an array from API response
const extractArray = (responseData: any, specificKey?: string): any[] => {
  if (Array.isArray(responseData)) {
    return responseData;
  }
  if (specificKey && responseData && Array.isArray(responseData[specificKey])) {
    return responseData[specificKey];
  }
  if (responseData && Array.isArray(responseData.data)) {
    return responseData.data; // Common wrapper key
  }
  if (responseData && Array.isArray(responseData.items)) {
    return responseData.items; // Another common wrapper key
  }
  // Add more specific key checks if needed for different endpoints
  // e.g. if users are under 'users_list', stations under 'station_list'
  return []; // Default to empty array if no array is found
};

export const DashboardProvider = ({ children }: { children: React.ReactNode }) => {
  const [batteries, setBatteries] = useState<Battery[]>([]);
  const [stations, setStations] = useState<Station[]>([]);
  const [swapActivities, setSwapActivities] = useState<SwapActivity[]>([]);
  const [users, setUsers] = useState<User[]>([]);

  useEffect(() => {
    // Fetch dashboard data from API
    const fetchDashboardData = async () => {
      try {
        // Fetch batteries
        const batteriesRes = await fetch('http://localhost:5000/api/batteries');
        const batteriesData = await batteriesRes.json();
        setBatteries(extractArray(batteriesData, 'batteries'));

        // Fetch stations
        const stationsRes = await fetch('http://localhost:5000/api/stations');
        const stationsData = await stationsRes.json();
        setStations(extractArray(stationsData, 'stations'));

        // Fetch swap activities
        const activitiesRes = await fetch('http://localhost:5000/api/swaps');
        const activitiesData = await activitiesRes.json();
        setSwapActivities(extractArray(activitiesData, 'swaps')); // Assuming 'swaps' might be a key, or 'swap_activities'

        // Fetch users
        const usersRes = await fetch('http://localhost:5000/api/users');
        if (!usersRes.ok) throw new Error(`Failed to fetch users: ${usersRes.statusText}`);
        const usersData = await usersRes.json();
        setUsers(extractArray(usersData, 'users'));

      } catch (error) {
        console.error('Error fetching dashboard data:', error);
        // Set empty arrays if fetch fails
        setBatteries([]);
        setStations([]);
        setSwapActivities([]);
        setUsers([]);
      }
    };

    fetchDashboardData();
    // Refresh data every 30 seconds
    const interval = setInterval(fetchDashboardData, 30000);
    return () => clearInterval(interval);
  }, []);

  return (
    <DashboardContext.Provider value={{ batteries, stations, swapActivities, users }}>
      {children}
    </DashboardContext.Provider>
  );
};

export const useDashboard = () => {
  const context = useContext(DashboardContext);
  if (context === undefined) {
    throw new Error('useDashboard must be used within a DashboardProvider');
  }
  return context;
};

// Types for the User model
export interface User {
  id: number;
  username: string;
  email: string;
  status: 'active' | 'inactive';
  createdAt: string;
  updatedAt: string;
}