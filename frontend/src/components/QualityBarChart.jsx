import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid,
} from "recharts";

export default function QualityBarChart({ checks }) {
  return (
    <div style={{ width: "100%", height: 320 }}>
      <ResponsiveContainer>
        <BarChart data={checks}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="check_name" />
          <YAxis />
          <Tooltip />
          <Bar dataKey="failed_rows" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
