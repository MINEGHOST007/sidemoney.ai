"use client";

import { useState } from "react";
import useSWR from "swr";
import { apiGet, apiPost } from "@/lib/api";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import {
  AlertCircle,
  TrendingUp,
  Target,
  CheckCircle2,
  Lightbulb,
  Brain,
} from "lucide-react";
import { formatCurrency } from "@/lib/utils";

type RecommendationType =
  | "budget_optimization"
  | "category_reduction"
  | "savings_increase"
  | "goal_acceleration"
  | "spending_pattern";

type RecommendationPriority = "high" | "medium" | "low";

type FinancialRecommendation = {
  title: string;
  description: string;
  type: RecommendationType;
  priority: RecommendationPriority;
  potential_savings?: number;
  action_items: string[];
  category_focus?: string;
};

type SpendingInsight = {
  insight_type: string;
  title: string;
  description: string;
  metric_value?: number;
  metric_unit?: string;
  trend_direction?: "up" | "down" | "stable";
  severity?: "low" | "medium" | "high";
};

type AIAnalysisResponse = {
  recommendations: FinancialRecommendation[];
  insights: SpendingInsight[];
  summary: string;
  confidence_score: number;
};

const PRIORITY_COLORS = {
  high: "bg-red-500/10 text-red-400 border-red-500/20",
  medium: "bg-yellow-500/10 text-yellow-400 border-yellow-500/20",
  low: "bg-green-500/10 text-green-400 border-green-500/20",
};

const TYPE_ICONS = {
  budget_optimization: TrendingUp,
  category_reduction: AlertCircle,
  savings_increase: Target,
  goal_acceleration: Target,
  spending_pattern: Brain,
};

const INSIGHT_ICONS = {
  trend: TrendingUp,
  pattern: Brain,
  comparison: TrendingUp,
  default: Lightbulb,
};

export function AIAnalysis() {
  const [loading, setLoading] = useState(false);
  const [periodDays, setPeriodDays] = useState(30);
  const [analysis, setAnalysis] = useState<AIAnalysisResponse | null>(null);

  const generateAnalysis = async () => {
    setLoading(true);
    try {
      const result = await apiPost<AIAnalysisResponse>(
        `/ai/analyze?period_days=${periodDays}`
      );

      // Log the response for debugging
      console.log("AI Analysis Response:", result);

      setAnalysis(result);
    } catch (error) {
      console.error("Failed to generate analysis:", error);
      // Show user-friendly error
      setAnalysis({
        recommendations: [],
        insights: [
          {
            insight_type: "pattern",
            title: "Analysis Error",
            description:
              "Unable to generate analysis at this time. Please try again.",
            trend_direction: "stable",
            severity: "medium",
          },
        ],
        summary:
          "Analysis temporarily unavailable. Please check your internet connection and try again.",
        confidence_score: 0.0,
      });
    } finally {
      setLoading(false);
    }
  };

  const getPriorityIcon = (priority: RecommendationPriority) => {
    switch (priority) {
      case "high":
        return AlertCircle;
      case "medium":
        return TrendingUp;
      case "low":
        return CheckCircle2;
      default:
        return Lightbulb;
    }
  };

  return (
    <div className="space-y-6">
      {/* Analysis Header */}
      <div className="bg-gradient-to-br from-[rgba(255,255,255,0.08)] to-[rgba(255,255,255,0.02)] rounded-2xl border border-white/10 p-6">
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
          <div className="flex items-center gap-3">
            <div className="w-12 h-12 rounded-xl bg-[rgb(0,255,178)]/10 flex items-center justify-center">
              <Brain className="h-6 w-6 text-[rgb(0,255,178)]" />
            </div>
            <div>
              <h3 className="text-xl font-semibold text-white">
                AI Financial Analysis
              </h3>
              <p className="text-white/60">
                Get personalized insights and recommendations
              </p>
            </div>
          </div>

          <div className="flex items-center gap-4">
            <Select
              value={periodDays.toString()}
              onValueChange={(value) => setPeriodDays(Number(value))}
            >
              <SelectTrigger className="w-[140px] bg-white/5 border-white/10 text-white hover:bg-white/10 focus:border-[rgb(0,255,178)]/50 [&>span]:text-white">
                <SelectValue />
              </SelectTrigger>
              <SelectContent className="bg-gray-900 border-white/10">
                <SelectItem
                  value="7"
                  className="text-white hover:bg-white/10 focus:bg-white/10 cursor-pointer"
                >
                  Last 7 days
                </SelectItem>
                <SelectItem
                  value="30"
                  className="text-white hover:bg-white/10 focus:bg-white/10 cursor-pointer"
                >
                  Last 30 days
                </SelectItem>
                <SelectItem
                  value="90"
                  className="text-white hover:bg-white/10 focus:bg-white/10 cursor-pointer"
                >
                  Last 90 days
                </SelectItem>
              </SelectContent>
            </Select>

            <Button
              onClick={generateAnalysis}
              disabled={loading}
              className="bg-[rgb(0,255,178)]/20 text-[rgb(0,255,178)] hover:bg-[rgb(0,255,178)]/30 border border-[rgb(0,255,178)]/30"
            >
              {loading ? "Analyzing..." : "Generate Analysis"}
            </Button>
          </div>
        </div>
      </div>

      {/* Analysis Results */}
      {analysis && (
        <div className="grid gap-6 lg:grid-cols-2">
          {/* Summary & Confidence */}
          <div className="lg:col-span-2">
            <Card className="bg-gradient-to-br from-[rgba(255,255,255,0.08)] to-[rgba(255,255,255,0.02)] border-white/10">
              <CardHeader>
                <div className="flex items-center justify-between">
                  <CardTitle className="text-white flex items-center gap-2">
                    <Lightbulb className="h-5 w-5 text-[rgb(0,255,178)]" />
                    Financial Health Summary
                  </CardTitle>
                  <Badge className={`${PRIORITY_COLORS.medium}`}>
                    {Math.round(analysis.confidence_score * 100)}% Confidence
                  </Badge>
                </div>
              </CardHeader>
              <CardContent>
                <p className="text-white/80 leading-relaxed">
                  {analysis.summary}
                </p>
              </CardContent>
            </Card>
          </div>

          {/* Recommendations */}
          <div>
            <Card className="bg-gradient-to-br from-[rgba(255,255,255,0.08)] to-[rgba(255,255,255,0.02)] border-white/10">
              <CardHeader>
                <CardTitle className="text-white flex items-center gap-2">
                  <Target className="h-5 w-5 text-[rgb(0,255,178)]" />
                  Recommendations ({analysis.recommendations.length})
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                {analysis.recommendations.length === 0 ? (
                  <p className="text-white/60 text-center py-8">
                    Great job! No specific recommendations at this time.
                  </p>
                ) : (
                  analysis.recommendations.map((rec, index) => {
                    const IconComponent = TYPE_ICONS[rec.type] || Lightbulb;
                    const PriorityIcon = getPriorityIcon(rec.priority);

                    return (
                      <div
                        key={index}
                        className="bg-white/5 rounded-lg p-4 border border-white/10"
                      >
                        <div className="flex items-start gap-3">
                          <div className="w-8 h-8 rounded-lg bg-[rgb(0,255,178)]/10 flex items-center justify-center flex-shrink-0">
                            <IconComponent className="h-4 w-4 text-[rgb(0,255,178)]" />
                          </div>
                          <div className="flex-1 min-w-0">
                            <div className="flex items-center gap-2 mb-2">
                              <h4 className="text-white font-medium">
                                {rec.title}
                              </h4>
                              <Badge
                                className={`text-xs ${
                                  PRIORITY_COLORS[rec.priority]
                                }`}
                              >
                                <PriorityIcon className="h-3 w-3 mr-1" />
                                {rec.priority}
                              </Badge>
                            </div>
                            <p className="text-white/70 text-sm mb-3 leading-relaxed">
                              {rec.description}
                            </p>

                            {rec.potential_savings &&
                              rec.potential_savings > 0 && (
                                <div className="mb-3">
                                  <Badge className="bg-green-500/10 text-green-400 border-green-500/20">
                                    💰 Potential savings:{" "}
                                    {formatCurrency(rec.potential_savings)}
                                    /month
                                  </Badge>
                                </div>
                              )}

                            {rec.action_items &&
                              rec.action_items.length > 0 && (
                                <div>
                                  <p className="text-white/60 text-xs font-medium mb-2 uppercase tracking-wide">
                                    Action Items:
                                  </p>
                                  <ul className="space-y-2">
                                    {rec.action_items
                                      .slice(0, 4)
                                      .map((item, i) => (
                                        <li
                                          key={i}
                                          className="text-white/70 text-sm flex items-start gap-2 bg-white/5 rounded px-2 py-1"
                                        >
                                          <CheckCircle2 className="h-4 w-4 text-[rgb(0,255,178)] mt-0.5 flex-shrink-0" />
                                          <span className="flex-1">{item}</span>
                                        </li>
                                      ))}
                                  </ul>
                                </div>
                              )}
                          </div>
                        </div>
                      </div>
                    );
                  })
                )}
              </CardContent>
            </Card>
          </div>

          {/* Insights */}
          <div>
            <Card className="bg-gradient-to-br from-[rgba(255,255,255,0.08)] to-[rgba(255,255,255,0.02)] border-white/10">
              <CardHeader>
                <CardTitle className="text-white flex items-center gap-2">
                  <TrendingUp className="h-5 w-5 text-[rgb(0,255,178)]" />
                  Spending Insights ({analysis.insights.length})
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                {analysis.insights.length === 0 ? (
                  <p className="text-white/60 text-center py-8">
                    No specific insights available for this period.
                  </p>
                ) : (
                  analysis.insights.map((insight, index) => {
                    const IconComponent =
                      INSIGHT_ICONS[
                        insight.insight_type as keyof typeof INSIGHT_ICONS
                      ] || INSIGHT_ICONS.default;

                    return (
                      <div
                        key={index}
                        className="bg-white/5 rounded-lg p-4 border border-white/10"
                      >
                        <div className="flex items-start gap-3">
                          <div className="w-8 h-8 rounded-lg bg-[rgb(0,255,178)]/10 flex items-center justify-center flex-shrink-0">
                            <IconComponent className="h-4 w-4 text-[rgb(0,255,178)]" />
                          </div>
                          <div className="flex-1 min-w-0">
                            <div className="flex items-center gap-2 mb-2">
                              <h4 className="text-white font-medium">
                                {insight.title}
                              </h4>
                              {insight.trend_direction && (
                                <Badge
                                  className={`text-xs ${
                                    insight.trend_direction === "up"
                                      ? "bg-red-500/10 text-red-400 border-red-500/20"
                                      : insight.trend_direction === "down"
                                      ? "bg-green-500/10 text-green-400 border-green-500/20"
                                      : "bg-gray-500/10 text-gray-400 border-gray-500/20"
                                  }`}
                                >
                                  {insight.trend_direction === "up"
                                    ? "↗"
                                    : insight.trend_direction === "down"
                                    ? "↘"
                                    : "→"}{" "}
                                  {insight.trend_direction}
                                </Badge>
                              )}
                            </div>
                            <p className="text-white/70 text-sm mb-3 leading-relaxed">
                              {insight.description}
                            </p>

                            {insight.metric_value !== undefined && (
                              <div className="flex items-center gap-3">
                                <div className="text-[rgb(0,255,178)] font-bold text-lg">
                                  {insight.metric_unit === "dollars" ||
                                  insight.metric_unit === "$"
                                    ? formatCurrency(insight.metric_value)
                                    : insight.metric_unit === "percent"
                                    ? `${insight.metric_value.toFixed(1)}%`
                                    : `${insight.metric_value}${
                                        insight.metric_unit || ""
                                      }`}
                                </div>
                                {insight.severity && (
                                  <Badge
                                    className={`text-xs ${
                                      insight.severity === "high"
                                        ? "bg-red-500/10 text-red-400 border-red-500/20"
                                        : insight.severity === "medium"
                                        ? "bg-yellow-500/10 text-yellow-400 border-yellow-500/20"
                                        : "bg-green-500/10 text-green-400 border-green-500/20"
                                    }`}
                                  >
                                    {insight.severity} impact
                                  </Badge>
                                )}
                              </div>
                            )}
                          </div>
                        </div>
                      </div>
                    );
                  })
                )}
              </CardContent>
            </Card>
          </div>
        </div>
      )}
    </div>
  );
}
