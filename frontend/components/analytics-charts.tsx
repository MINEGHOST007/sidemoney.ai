"use client"

import { formatCurrency } from "@/lib/utils"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { ResponsiveContainer, BarChart, Bar, XAxis, YAxis, Tooltip, PieChart, Pie, Cell, Legend } from "recharts"

export function AnalyticsCharts({ report }: { report?: any }) {
  const categoryData = report
    ? Object.entries(report.category_breakdown || {}).map(([name, value]) => ({ 
        name: name.replace(/_/g, ' ').toLowerCase().replace(/\b\w/g, l => l.toUpperCase()), 
        value 
      }))
    : []

  const netData = report
    ? [
        { name: "Income", value: Number(report.total_income || 0), fill: "rgb(0,255,178)" },
        { name: "Expenses", value: Number(report.total_expenses || 0), fill: "#F59E0B" },
      ]
    : []

  const COLORS = ["rgb(0,255,178)", "#10B981", "#F59E0B", "#A855F7", "#8B5CF6", "#06B6D4", "#EC4899", "#F97316"]

  // Custom legend render function for pie chart
  const renderCustomPieLegend = (props: any) => {
    const { payload } = props;
    return (
      <div className="flex flex-wrap gap-3 justify-center mt-4">
        {payload.map((entry: any, index: number) => (
          <div key={index} className="flex items-center gap-2">
            <div 
              className="w-3 h-3 rounded-full" 
              style={{ backgroundColor: entry.color }}
            />
            <span className="text-sm text-white font-semibold drop-shadow-lg">{entry.value}</span>
          </div>
        ))}
      </div>
    );
  }

  // Custom label function for pie chart
  const renderCustomLabel = ({ cx, cy, midAngle, innerRadius, outerRadius, percent }: any) => {
    if (percent < 0.05) return null; // Don't show labels for slices smaller than 5%
    
    const RADIAN = Math.PI / 180;
    const radius = innerRadius + (outerRadius - innerRadius) * 0.5;
    const x = cx + radius * Math.cos(-midAngle * RADIAN);
    const y = cy + radius * Math.sin(-midAngle * RADIAN);

    return (
      <text 
        x={x} 
        y={y} 
        fill="white" 
        textAnchor={x > cx ? 'start' : 'end'} 
        dominantBaseline="central"
        fontSize="13"
        fontWeight="700"
        stroke="rgba(8,7,14,0.9)"
        strokeWidth="3"
        paintOrder="stroke fill"
        style={{ filter: 'drop-shadow(0 0 4px rgba(0,0,0,0.8))' }}
      >
        {`${(percent * 100).toFixed(0)}%`}
      </text>
    );
  }

  return (
    <>
      <style jsx global>{`
        /* Remove gray hover overlays and use light green theme */
        .recharts-active-shape {
          filter: drop-shadow(0 0 8px rgba(0,255,178,0.4)) brightness(1.1) !important;
          opacity: 1 !important;
        }
        
        .recharts-sector:hover {
          filter: drop-shadow(0 0 8px rgba(0,255,178,0.4)) brightness(1.1) !important;
          opacity: 1 !important;
          stroke: rgba(0,255,178,0.6) !important;
          stroke-width: 2px !important;
        }
        
        .recharts-rectangle:hover {
          filter: drop-shadow(0 0 8px rgba(0,255,178,0.4)) brightness(1.1) !important;
          opacity: 1 !important;
          stroke: rgba(0,255,178,0.6) !important;
          stroke-width: 2px !important;
        }
        
        /* Remove all default hover states and gray overlays */
        .recharts-bar:hover .recharts-rectangle,
        .recharts-bar .recharts-rectangle:hover {
          fill-opacity: 1 !important;
          stroke-opacity: 1 !important;
          opacity: 1 !important;
        }
        
        .recharts-pie-sector:hover,
        .recharts-pie .recharts-sector:hover {
          fill-opacity: 1 !important;
          stroke-opacity: 1 !important;
          opacity: 1 !important;
        }
        
        /* Override any active/hover shape overlays */
        .recharts-active-shape rect,
        .recharts-active-shape path {
          fill-opacity: 1 !important;
          opacity: 1 !important;
        }
        
        /* Remove gray backgrounds from tooltips */
        .recharts-default-tooltip,
        .recharts-tooltip-wrapper {
          background-color: rgba(8,7,14,0.95) !important;
          border: 1px solid rgba(0,255,178,0.5) !important;
          color: #ffffff !important;
          opacity: 1 !important;
        }
        
        /* Remove any gray hover animations */
        .recharts-surface {
          background: transparent !important;
        }
        
        /* Ensure no gray overlays on active elements */
        .recharts-layer .recharts-active-dot {
          stroke: rgb(0,255,178) !important;
          fill: rgb(0,255,178) !important;
          opacity: 1 !important;
        }
        
        /* Override any Recharts default hover animations */
        .recharts-wrapper .recharts-surface g {
          opacity: 1 !important;
        }
        
        /* Force remove any gray overlay masks */
        .recharts-sector,
        .recharts-rectangle {
          transition: filter 0.2s ease !important;
        }
        
        .recharts-sector:hover,
        .recharts-rectangle:hover {
          filter: drop-shadow(0 0 12px rgba(0,255,178,0.6)) brightness(1.15) saturate(1.1) !important;
        }
        
        /* Additional light green glow effects */
        .recharts-pie .recharts-sector:hover {
          filter: drop-shadow(0 0 10px rgba(0,255,178,0.5)) brightness(1.1) !important;
        }
        
        .recharts-bar .recharts-rectangle:hover {
          filter: drop-shadow(0 0 10px rgba(0,255,178,0.5)) brightness(1.1) !important;
        }
      `}</style>
      
      <div className="grid gap-6 md:grid-cols-2">
        <div className="bg-gradient-to-br from-[rgba(255,255,255,0.08)] to-[rgba(255,255,255,0.02)] rounded-2xl border border-white/10 p-6">
          <h3 className="text-xl font-semibold text-white mb-6">Category Breakdown</h3>
          <div className="h-80">
            {categoryData.length > 0 ? (
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie 
                    data={categoryData} 
                    dataKey="value" 
                    nameKey="name" 
                    outerRadius={80} 
                    innerRadius={40}
                    strokeWidth={2}
                    stroke="rgba(255,255,255,0.1)"
                    label={renderCustomLabel}
                    labelLine={false}
                    animationBegin={0}
                    animationDuration={800}
                    style={{ cursor: 'pointer' }}
                  >
                    {categoryData.map((_, idx) => (
                      <Cell 
                        key={idx} 
                        fill={COLORS[idx % COLORS.length]}
                        stroke="rgba(255,255,255,0.2)"
                        strokeWidth={1}
                        style={{ 
                          filter: 'brightness(1)',
                          transition: 'all 0.2s ease'
                        }}
                      />
                    ))}
                  </Pie>
                  <Tooltip 
                    contentStyle={{
                      backgroundColor: 'rgba(8,7,14,0.95)',
                      border: '1px solid rgba(0,255,178,0.5)',
                      borderRadius: '12px',
                      color: '#ffffff',
                      boxShadow: '0 10px 25px rgba(0,0,0,0.8)',
                      fontSize: '14px',
                      fontWeight: '600'
                    }}
                    formatter={(value: any, name: any) => [
                      <span style={{ color: '#ffffff', fontWeight: '700' }}>{formatCurrency(Number(value))}</span>, 
                      <span style={{ color: '#ffffff', fontWeight: '600' }}>{name}</span>
                    ]}
                    labelStyle={{ color: 'rgb(0,255,178)', fontWeight: '700', fontSize: '14px' }}
                  />
                  <Legend content={renderCustomPieLegend} />
                </PieChart>
              </ResponsiveContainer>
            ) : (
              <div className="flex items-center justify-center h-full">
                <div className="text-center">
                  <div className="w-16 h-16 rounded-full bg-white/5 flex items-center justify-center mx-auto mb-4">
                    📊
                  </div>
                  <p className="text-white/60">No expense data available</p>
                  <p className="text-sm text-white/40">Add some transactions to see the breakdown</p>
                </div>
              </div>
            )}
          </div>
        </div>

        <div className="bg-gradient-to-br from-[rgba(255,255,255,0.08)] to-[rgba(255,255,255,0.02)] rounded-2xl border border-white/10 p-6">
          <h3 className="text-xl font-semibold text-white mb-6">Income vs Expenses</h3>
          <div className="h-80">
            {netData.some(item => item.value > 0) ? (
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={netData} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
                  <XAxis 
                    dataKey="name" 
                    tick={{ fill: '#ffffff', fontSize: 14, fontWeight: '600' }}
                    axisLine={{ stroke: 'rgba(255,255,255,0.4)' }}
                    tickLine={{ stroke: 'rgba(255,255,255,0.4)' }}
                  />
                  <YAxis 
                    tick={{ fill: '#ffffff', fontSize: 12, fontWeight: '600' }}
                    axisLine={{ stroke: 'rgba(255,255,255,0.4)' }}
                    tickLine={{ stroke: 'rgba(255,255,255,0.4)' }}
                    tickFormatter={(value) => formatCurrency(value)}
                  />
                  <Tooltip 
                    contentStyle={{
                      backgroundColor: 'rgba(8,7,14,0.95)',
                      border: '1px solid rgba(0,255,178,0.5)',
                      borderRadius: '12px',
                      color: '#ffffff',
                      boxShadow: '0 10px 25px rgba(0,0,0,0.8)',
                      fontSize: '14px',
                      fontWeight: '600'
                    }}
                    formatter={(value: any) => [
                      <span style={{ color: '#ffffff', fontWeight: '700' }}>{formatCurrency(Number(value))}</span>, 
                      ''
                    ]}
                    labelStyle={{ color: 'rgb(0,255,178)', fontWeight: '700', fontSize: '14px' }}
                  />
                  <Bar 
                    dataKey="value" 
                    radius={[8, 8, 0, 0]} 
                    stroke="rgba(255,255,255,0.1)"
                    strokeWidth={1}
                  />
                </BarChart>
              </ResponsiveContainer>
            ) : (
              <div className="flex items-center justify-center h-full">
                <div className="text-center">
                  <div className="w-16 h-16 rounded-full bg-white/5 flex items-center justify-center mx-auto mb-4">
                    💰
                  </div>
                  <p className="text-white/60">No financial data available</p>
                  <p className="text-sm text-white/40">Add income and expense transactions to see the comparison</p>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </>
  )
}
