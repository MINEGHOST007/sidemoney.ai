"use client";

import type React from "react";
import { useState, useEffect } from "react";
import useSWRMutation from "swr/mutation";
import { apiPost } from "@/lib/api";
import { formatCurrency } from "@/lib/utils";
import { useCacheInvalidation } from "@/hooks/use-cache-invalidation";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import { useToast } from "@/hooks/use-toast";
import {
  Calendar,
  DollarSign,
  Tag,
  FileText,
  Plus,
  Loader2,
  Sparkles,
} from "lucide-react";

const categories = [
  {
    value: "FOOD_DINING",
    label: "Food & Dining",
    color: "from-orange-500 to-amber-500",
  },
  {
    value: "GROCERIES",
    label: "Groceries",
    color: "from-green-500 to-emerald-500",
  },
  {
    value: "TRANSPORTATION",
    label: "Transportation",
    color: "from-blue-500 to-indigo-500",
  },
  {
    value: "SHOPPING",
    label: "Shopping",
    color: "from-purple-500 to-pink-500",
  },
  {
    value: "ENTERTAINMENT",
    label: "Entertainment",
    color: "from-pink-500 to-rose-500",
  },
  {
    value: "BILLS_UTILITIES",
    label: "Bills & Utilities",
    color: "from-yellow-500 to-orange-500",
  },
  {
    value: "HEALTHCARE",
    label: "Healthcare",
    color: "from-blue-500 to-purple-500",
  },
  {
    value: "EDUCATION",
    label: "Education",
    color: "from-indigo-500 to-purple-500",
  },
  { value: "TRAVEL", label: "Travel", color: "from-cyan-500 to-blue-500" },
  {
    value: "FITNESS",
    label: "Fitness",
    color: "from-emerald-500 to-green-500",
  },
  {
    value: "PERSONAL_CARE",
    label: "Personal Care",
    color: "from-teal-500 to-cyan-500",
  },
  {
    value: "GIFTS_DONATIONS",
    label: "Gifts & Donations",
    color: "from-rose-500 to-pink-500",
  },
  { value: "BUSINESS", label: "Business", color: "from-slate-500 to-gray-500" },
  {
    value: "MISCELLANEOUS",
    label: "Miscellaneous",
    color: "from-gray-500 to-slate-500",
  },
];

interface CategorizeResponse {
  suggested_category?: string;
}

interface TransactionFormProps {
  trigger?: React.ReactNode;
}

export function TransactionForm({ trigger }: TransactionFormProps) {
  const [open, setOpen] = useState(false);
  const [type, setType] = useState<"income" | "expense">("expense");
  const [category, setCategory] = useState("");
  const [amount, setAmount] = useState("");
  const [date, setDate] = useState(new Date().toLocaleDateString("en-CA"));
  const [description, setDescription] = useState("");
  const [isCategorizing, setIsCategorizing] = useState(false);
  const [errors, setErrors] = useState<Record<string, string>>({});
  const { toast } = useToast();
  const { invalidateTransactionData } = useCacheInvalidation();

  // Create transaction mutation
  const { trigger: createTransaction, isMutating } = useSWRMutation(
    "/transactions",
    async (_key, { arg }: { arg: any }) => {
      return apiPost("/transactions", arg);
    }
  );

  // Auto-categorization effect
  useEffect(() => {
    if (
      type === "expense" &&
      description.trim().length > 3 &&
      amount &&
      parseFloat(amount) > 0
    ) {
      const timeoutId = setTimeout(async () => {
        setIsCategorizing(true);
        try {
          // Call the categorization API with params
          const params = new URLSearchParams({
            description: description.trim(),
            amount: amount,
          });
          const response = await apiPost<CategorizeResponse>(
            `/transactions/categorize?${params.toString()}`,
            null,
            true
          );

          if (response?.suggested_category) {
            setCategory(response.suggested_category);
            const categoryLabel = categories.find(
              (c) => c.value === response.suggested_category
            )?.label;
            toast({
              title: "Category Suggested",
              description: `Auto-categorized as "${categoryLabel}"`,
            });
          }
        } catch (error) {
          // Silently fail - categorization is optional
          console.log("Auto-categorization failed:", error);
        } finally {
          setIsCategorizing(false);
        }
      }, 1000); // Debounce for 1 second

      return () => clearTimeout(timeoutId);
    }
  }, [description, amount, type, toast]);

  const validateForm = () => {
    const newErrors: Record<string, string> = {};

    if (!description.trim()) {
      newErrors.description = "Description is required";
    }

    const amt = parseFloat(amount);
    if (!amount || amt <= 0) {
      newErrors.amount = "Amount must be greater than 0";
    }

    if (!date) {
      newErrors.date = "Date is required";
    }

    if (type === "expense" && !category) {
      newErrors.category = "Category is required for expenses";
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const resetForm = () => {
    setType("expense");
    setCategory("");
    setAmount("");
    setDescription("");
    setDate(new Date().toLocaleDateString("en-CA"));
    setErrors({});
  };

  async function onSubmit(e: React.FormEvent) {
    e.preventDefault();

    if (!validateForm()) {
      return;
    }

    try {
      await createTransaction({
        amount: parseFloat(amount),
        type,
        category: type === "expense" ? category : null,
        description: description.trim(),
        date,
      });

      // Invalidate all dependent caches to trigger refetch
      await invalidateTransactionData();

      toast({
        title: "Success!",
        description: `${
          type === "income" ? "Income" : "Expense"
        } transaction added successfully`,
      });

      resetForm();
      setOpen(false);
    } catch (error) {
      console.error("Transaction creation error:", error);
      toast({
        title: "Error",
        description:
          error instanceof Error
            ? error.message
            : "Failed to create transaction. Please try again.",
        variant: "destructive",
      });
    }
  }

  const defaultTrigger = (
    <Button className="bg-[rgb(0,255,178)] text-black hover:bg-[rgb(0,255,178)]/90 font-semibold rounded-full px-6 py-3 shadow-lg shadow-[rgb(0,255,178)]/20 flex items-center gap-2">
      <Plus className="h-4 w-4" />
      Add Transaction
    </Button>
  );

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger asChild>{trigger || defaultTrigger}</DialogTrigger>
      <DialogContent className="bg-[rgb(8,7,14)] border-white/20 text-white max-w-md">
        <DialogHeader>
          <DialogTitle className="text-2xl font-bold text-white flex items-center gap-2">
            <Plus className="h-6 w-6 text-[rgb(0,255,178)]" />
            Add Transaction
          </DialogTitle>
        </DialogHeader>

        <form onSubmit={onSubmit} className="space-y-4">
          <div className="space-y-4">
            {/* Transaction Type */}
            <div className="grid gap-2">
              <Label className="text-white/90 font-medium flex items-center gap-2">
                <Tag className="h-4 w-4 text-[rgb(0,255,178)]" />
                Transaction Type
              </Label>
              <Select value={type} onValueChange={(v: any) => setType(v)}>
                <SelectTrigger className="bg-white/5 border-white/20 text-white hover:bg-white/10 focus:ring-[rgb(0,255,178)]/50">
                  <SelectValue />
                </SelectTrigger>
                <SelectContent className="bg-[rgb(8,7,14)] border-white/20">
                  <SelectItem
                    value="income"
                    className="text-white hover:bg-white/10 focus:bg-white/10"
                  >
                    Income
                  </SelectItem>
                  <SelectItem
                    value="expense"
                    className="text-white hover:bg-white/10 focus:bg-white/10"
                  >
                    Expense
                  </SelectItem>
                </SelectContent>
              </Select>
            </div>

            {/* Description - Mandatory */}
            <div className="grid gap-2">
              <Label className="text-white/90 font-medium flex items-center gap-2">
                <FileText className="h-4 w-4 text-[rgb(0,255,178)]" />
                Description *
              </Label>
              <Input
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                placeholder="What was this transaction for?"
                className="bg-white/5 border-white/20 text-white placeholder:text-white/50 hover:bg-white/10 focus:ring-[rgb(0,255,178)]/50 focus:border-[rgb(0,255,178)]/50"
              />
              {errors.description && (
                <p className="text-white/70 text-sm">{errors.description}</p>
              )}
            </div>

            {/* Amount */}
            <div className="grid gap-2">
              <Label className="text-white/90 font-medium flex items-center gap-2">
                <DollarSign className="h-4 w-4 text-[rgb(0,255,178)]" />
                Amount (₹) *
              </Label>
              <Input
                type="number"
                step="0.01"
                value={amount}
                onChange={(e) => setAmount(e.target.value)}
                placeholder="500.00"
                className="bg-white/5 border-white/20 text-white placeholder:text-white/50 hover:bg-white/10 focus:ring-[rgb(0,255,178)]/50 focus:border-[rgb(0,255,178)]/50"
              />
              {errors.amount && (
                <p className="text-white/70 text-sm">{errors.amount}</p>
              )}
            </div>

            {/* Category - Only for expenses with auto-categorization */}
            {type === "expense" && (
              <div className="grid gap-2">
                <Label className="text-white/90 font-medium flex items-center gap-2">
                  <Tag className="h-4 w-4 text-[rgb(0,255,178)]" />
                  Category *
                  {isCategorizing && (
                    <div className="flex items-center gap-1 text-xs text-[rgb(0,255,178)]">
                      <Loader2 className="h-3 w-3 animate-spin" />
                      <Sparkles className="h-3 w-3" />
                      Auto-categorizing...
                    </div>
                  )}
                </Label>
                <Select value={category} onValueChange={setCategory}>
                  <SelectTrigger className="bg-white/5 border-white/20 text-white hover:bg-white/10 focus:ring-[rgb(0,255,178)]/50">
                    <SelectValue placeholder="Select category" />
                  </SelectTrigger>
                  <SelectContent className="bg-[rgb(8,7,14)] border-white/20 max-h-60">
                    {categories.map((c) => (
                      <SelectItem
                        key={c.value}
                        value={c.value}
                        className="text-white hover:bg-white/10 focus:bg-white/10"
                      >
                        {c.label}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
                {errors.category && (
                  <p className="text-white/70 text-sm">{errors.category}</p>
                )}
              </div>
            )}

            {/* Date */}
            <div className="grid gap-2">
              <Label className="text-white/90 font-medium flex items-center gap-2">
                <Calendar className="h-4 w-4 text-[rgb(0,255,178)]" />
                Date *
              </Label>
              <Input
                type="date"
                value={date}
                onChange={(e) => setDate(e.target.value)}
                className="bg-white/5 border-white/20 text-white hover:bg-white/10 focus:ring-[rgb(0,255,178)]/50 focus:border-[rgb(0,255,178)]/50"
              />
              {errors.date && (
                <p className="text-white/70 text-sm">{errors.date}</p>
              )}
            </div>
          </div>

          {/* Form Actions */}
          <div className="flex gap-3 pt-4">
            <Button
              type="button"
              variant="outline"
              onClick={() => setOpen(false)}
              className="flex-1 bg-transparent border-white/20 text-white hover:bg-white/10"
            >
              Cancel
            </Button>
            <Button
              type="submit"
              disabled={isMutating}
              className="flex-1 bg-[rgb(0,255,178)] text-black hover:bg-[rgb(0,255,178)]/90 font-semibold rounded-xl shadow-lg shadow-[rgb(0,255,178)]/20 transition-all duration-200 hover:shadow-[rgb(0,255,178)]/30"
            >
              {isMutating ? (
                <div className="flex items-center gap-2">
                  <Loader2 className="w-4 h-4 animate-spin" />
                  Saving...
                </div>
              ) : (
                `Add ${type === "income" ? "Income" : "Expense"}`
              )}
            </Button>
          </div>
        </form>
      </DialogContent>
    </Dialog>
  );
}
