"use client";

import { useState } from "react";
import { apiPost } from "@/lib/api";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import { Checkbox } from "@/components/ui/checkbox";
import {
  MessageSquare,
  Send,
  Bot,
  User,
  Lightbulb,
  Database,
  Clock,
} from "lucide-react";

type AIPromptRequest = {
  user_query: string;
  include_transactions: boolean;
  include_goals: boolean;
  include_budget: boolean;
  period_days: number;
};

type AIPromptResponse = {
  response: string;
  data_sources: string[];
  suggestions: string[];
  confidence: number;
};

type ChatMessage = {
  id: string;
  type: "user" | "ai";
  content: string;
  timestamp: Date;
  confidence?: number;
  data_sources?: string[];
  suggestions?: string[];
};

export function AIQuery() {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [currentQuery, setCurrentQuery] = useState("");
  const [loading, setLoading] = useState(false);

  // Query settings
  const [includeTransactions, setIncludeTransactions] = useState(true);
  const [includeGoals, setIncludeGoals] = useState(true);
  const [includeBudget, setIncludeBudget] = useState(true);
  const [periodDays, setPeriodDays] = useState(30);

  const sendQuery = async () => {
    if (!currentQuery.trim() || loading) return;

    const userMessage: ChatMessage = {
      id: Date.now().toString(),
      type: "user",
      content: currentQuery,
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setCurrentQuery("");
    setLoading(true);

    try {
      const request: AIPromptRequest = {
        user_query: currentQuery,
        include_transactions: includeTransactions,
        include_goals: includeGoals,
        include_budget: includeBudget,
        period_days: periodDays,
      };

      const response = await apiPost<AIPromptResponse>("/ai/query", request);

      const aiMessage: ChatMessage = {
        id: (Date.now() + 1).toString(),
        type: "ai",
        content: response.response,
        timestamp: new Date(),
        confidence: response.confidence,
        data_sources: response.data_sources,
        suggestions: response.suggestions,
      };

      setMessages((prev) => [...prev, aiMessage]);
    } catch (error) {
      console.error("Failed to send query:", error);

      const errorMessage: ChatMessage = {
        id: (Date.now() + 1).toString(),
        type: "ai",
        content:
          "I'm sorry, I encountered an error processing your request. Please try again.",
        timestamp: new Date(),
        confidence: 0,
      };

      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendQuery();
    }
  };

  const clearChat = () => {
    setMessages([]);
  };

  const suggestionQueries = [
    "How much did I spend on dining out this month?",
    "Am I on track to meet my savings goals?",
    "What categories am I overspending in?",
    "Show me my spending trends over the past few months",
    "How can I optimize my budget?",
    "What's my biggest expense category?",
  ];

  return (
    <div className="space-y-6">
      {/* Query Header & Settings */}
      <div className="bg-gradient-to-br from-[rgba(255,255,255,0.08)] to-[rgba(255,255,255,0.02)] rounded-2xl border border-white/10 p-6">
        <div className="flex flex-col gap-6">
          {/* Header */}
          <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
            <div className="flex items-center gap-3">
              <div className="w-12 h-12 rounded-xl bg-[rgb(0,255,178)]/10 flex items-center justify-center">
                <MessageSquare className="h-6 w-6 text-[rgb(0,255,178)]" />
              </div>
              <div>
                <h3 className="text-xl font-semibold text-white">
                  AI Financial Assistant
                </h3>
                <p className="text-white/60">
                  Ask questions about your financial data
                </p>
              </div>
            </div>

            <div className="flex items-center gap-3">
              <select
                value={periodDays}
                onChange={(e) => setPeriodDays(Number(e.target.value))}
                className="bg-white/5 border border-white/10 rounded-lg px-3 py-2 text-white text-sm focus:outline-none focus:border-[rgb(0,255,178)]/50"
              >
                <option value={7}>Last 7 days</option>
                <option value={30}>Last 30 days</option>
                <option value={90}>Last 90 days</option>
                <option value={365}>Last year</option>
              </select>

              {messages.length > 0 && (
                <Button
                  onClick={clearChat}
                  variant="outline"
                  size="sm"
                  className="border-white/20 text-white/60 hover:text-white hover:border-white/40"
                >
                  Clear Chat
                </Button>
              )}
            </div>
          </div>

          {/* Data Source Settings */}
          <div className="flex flex-wrap gap-4">
            <div className="flex items-center gap-2">
              <Checkbox
                id="transactions"
                checked={includeTransactions}
                onCheckedChange={(checked) =>
                  setIncludeTransactions(checked === true)
                }
                className="border-white/30 data-[state=checked]:bg-[rgb(0,255,178)] data-[state=checked]:border-[rgb(0,255,178)]"
              />
              <label htmlFor="transactions" className="text-white/70 text-sm">
                Include Transactions
              </label>
            </div>

            <div className="flex items-center gap-2">
              <Checkbox
                id="goals"
                checked={includeGoals}
                onCheckedChange={(checked) => setIncludeGoals(checked === true)}
                className="border-white/30 data-[state=checked]:bg-[rgb(0,255,178)] data-[state=checked]:border-[rgb(0,255,178)]"
              />
              <label htmlFor="goals" className="text-white/70 text-sm">
                Include Goals
              </label>
            </div>

            <div className="flex items-center gap-2">
              <Checkbox
                id="budget"
                checked={includeBudget}
                onCheckedChange={(checked) =>
                  setIncludeBudget(checked === true)
                }
                className="border-white/30 data-[state=checked]:bg-[rgb(0,255,178)] data-[state=checked]:border-[rgb(0,255,178)]"
              />
              <label htmlFor="budget" className="text-white/70 text-sm">
                Include Budget
              </label>
            </div>
          </div>
        </div>
      </div>

      {/* Chat Interface */}
      <div className="bg-gradient-to-br from-[rgba(255,255,255,0.08)] to-[rgba(255,255,255,0.02)] rounded-2xl border border-white/10 overflow-hidden">
        {/* Messages */}
        <div className="p-6 space-y-4 max-h-96 overflow-y-auto">
          {messages.length === 0 ? (
            <div className="text-center py-8">
              <Bot className="h-12 w-12 text-[rgb(0,255,178)] mx-auto mb-4 opacity-50" />
              <p className="text-white/60 mb-4">
                Ask me anything about your finances!
              </p>

              {/* Quick Suggestions */}
              <div className="grid gap-2 max-w-lg mx-auto">
                <p className="text-white/40 text-sm mb-2">Try asking:</p>
                {suggestionQueries.slice(0, 3).map((suggestion, index) => (
                  <button
                    key={index}
                    onClick={() => setCurrentQuery(suggestion)}
                    className="text-left p-2 rounded-lg bg-white/5 hover:bg-white/10 border border-white/10 hover:border-[rgb(0,255,178)]/30 transition-colors text-white/70 text-sm"
                  >
                    "{suggestion}"
                  </button>
                ))}
              </div>
            </div>
          ) : (
            messages.map((message) => (
              <div
                key={message.id}
                className={`flex gap-3 ${
                  message.type === "user" ? "justify-end" : "justify-start"
                }`}
              >
                <div
                  className={`flex gap-3 max-w-[80%] ${
                    message.type === "user" ? "flex-row-reverse" : "flex-row"
                  }`}
                >
                  <div
                    className={`w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0 ${
                      message.type === "user"
                        ? "bg-[rgb(0,255,178)]/20"
                        : "bg-purple-500/20"
                    }`}
                  >
                    {message.type === "user" ? (
                      <User className="h-4 w-4 text-[rgb(0,255,178)]" />
                    ) : (
                      <Bot className="h-4 w-4 text-purple-400" />
                    )}
                  </div>

                  <div
                    className={`rounded-2xl p-4 ${
                      message.type === "user"
                        ? "bg-[rgb(0,255,178)]/10 border border-[rgb(0,255,178)]/20"
                        : "bg-white/5 border border-white/10"
                    }`}
                  >
                    <div className="flex items-center gap-2 mb-2">
                      <span
                        className={`font-medium text-sm ${
                          message.type === "user"
                            ? "text-[rgb(0,255,178)]"
                            : "text-purple-400"
                        }`}
                      >
                        {message.type === "user" ? "You" : "AI Assistant"}
                      </span>
                      <span className="text-white/40 text-xs">
                        {message.timestamp.toLocaleTimeString()}
                      </span>
                    </div>

                    <p className="text-white/80 whitespace-pre-wrap leading-relaxed">
                      {message.content}
                    </p>

                    {message.type === "ai" && (
                      <div className="mt-3 space-y-2">
                        {/* Confidence Score */}
                        {message.confidence !== undefined && (
                          <Badge className="bg-white/10 text-white/60 border-white/20 text-xs">
                            {Math.round(message.confidence * 100)}% confidence
                          </Badge>
                        )}

                        {/* Data Sources */}
                        {message.data_sources &&
                          message.data_sources.length > 0 && (
                            <div className="flex items-center gap-2">
                              <Database className="h-3 w-3 text-white/40" />
                              <span className="text-white/40 text-xs">
                                Used: {message.data_sources.join(", ")}
                              </span>
                            </div>
                          )}

                        {/* Suggestions */}
                        {message.suggestions &&
                          message.suggestions.length > 0 && (
                            <div className="mt-3">
                              <div className="flex items-center gap-2 mb-2">
                                <Lightbulb className="h-3 w-3 text-[rgb(0,255,178)]" />
                                <span className="text-white/60 text-xs">
                                  Follow-up suggestions:
                                </span>
                              </div>
                              <div className="space-y-1">
                                {message.suggestions.map(
                                  (suggestion, index) => (
                                    <button
                                      key={index}
                                      onClick={() =>
                                        setCurrentQuery(suggestion)
                                      }
                                      className="block w-full text-left p-2 rounded-lg bg-white/5 hover:bg-white/10 border border-white/10 hover:border-[rgb(0,255,178)]/30 transition-colors text-white/60 text-xs"
                                    >
                                      {suggestion}
                                    </button>
                                  )
                                )}
                              </div>
                            </div>
                          )}
                      </div>
                    )}
                  </div>
                </div>
              </div>
            ))
          )}

          {/* Loading indicator */}
          {loading && (
            <div className="flex gap-3 justify-start">
              <div className="w-8 h-8 rounded-full bg-purple-500/20 flex items-center justify-center flex-shrink-0">
                <Bot className="h-4 w-4 text-purple-400" />
              </div>
              <div className="bg-white/5 border border-white/10 rounded-2xl p-4">
                <div className="flex items-center gap-2">
                  <div className="flex space-x-1">
                    <div className="w-2 h-2 bg-[rgb(0,255,178)] rounded-full animate-bounce"></div>
                    <div className="w-2 h-2 bg-[rgb(0,255,178)] rounded-full animate-bounce delay-100"></div>
                    <div className="w-2 h-2 bg-[rgb(0,255,178)] rounded-full animate-bounce delay-200"></div>
                  </div>
                  <span className="text-white/60 text-sm">Thinking...</span>
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Input */}
        <div className="border-t border-white/10 p-4">
          <div className="flex gap-3">
            <Input
              value={currentQuery}
              onChange={(e) => setCurrentQuery(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Ask me about your spending, goals, or any financial question..."
              className="flex-1 bg-white/5 border-white/20 text-white placeholder:text-white/40 focus:border-[rgb(0,255,178)]/50"
              disabled={loading}
            />
            <Button
              onClick={sendQuery}
              disabled={!currentQuery.trim() || loading}
              className="bg-[rgb(0,255,178)]/20 text-[rgb(0,255,178)] hover:bg-[rgb(0,255,178)]/30 border border-[rgb(0,255,178)]/30"
            >
              <Send className="h-4 w-4" />
            </Button>
          </div>
        </div>
      </div>
    </div>
  );
}
