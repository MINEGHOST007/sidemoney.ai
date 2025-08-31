"use client";

import { useMemo, useState } from "react";
import useSWR from "swr";
import { apiDelete, apiGet } from "@/lib/api";
import { formatCurrency } from "@/lib/utils";
import { useCacheInvalidation } from "@/hooks/use-cache-invalidation";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import {
  Select,
  SelectTrigger,
  SelectContent,
  SelectItem,
  SelectValue,
} from "@/components/ui/select";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { useToast } from "@/hooks/use-toast";
import {
  Trash2,
  Search,
  Filter,
  Calendar,
  DollarSign,
  Tag,
  FileText,
  TrendingUp,
  TrendingDown,
} from "lucide-react";

type Transaction = {
  id: string;
  user_id: string;
  amount: number;
  type: "income" | "expense";
  category?: string | null;
  description?: string;
  date: string;
  created_at?: string;
  updated_at?: string;
};

type TxnResponse = {
  transactions: Transaction[];
  total: number;
  page: number;
  per_page: number;
  total_pages: number;
};

const categories = [
  { value: "FOOD_DINING", label: "Food & Dining" },
  { value: "GROCERIES", label: "Groceries" },
  { value: "TRANSPORTATION", label: "Transportation" },
  { value: "SHOPPING", label: "Shopping" },
  { value: "ENTERTAINMENT", label: "Entertainment" },
  { value: "BILLS_UTILITIES", label: "Bills & Utilities" },
  { value: "HEALTHCARE", label: "Healthcare" },
  { value: "EDUCATION", label: "Education" },
  { value: "TRAVEL", label: "Travel" },
  { value: "FITNESS", label: "Fitness" },
  { value: "PERSONAL_CARE", label: "Personal Care" },
  { value: "GIFTS_DONATIONS", label: "Gifts & Donations" },
  { value: "BUSINESS", label: "Business" },
  { value: "MISCELLANEOUS", label: "Miscellaneous" },
];

export function TransactionsTable() {
  const [page, setPage] = useState(1);
  const [type, setType] = useState<string>("all");
  const [category, setCategory] = useState<string>("all");
  const [search, setSearch] = useState("");
  const { toast } = useToast();
  const { invalidateTransactionData } = useCacheInvalidation();

  const query = useMemo(() => {
    const p = new URLSearchParams({ page: String(page), per_page: "10" });
    if (type !== "all") p.set("transaction_type", type);
    if (category !== "all") p.set("category", category);
    if (search) p.set("search", search);
    return `/transactions?${p.toString()}`;
  }, [page, type, category, search]);

  const { data, mutate: mutateTransactions, isLoading } = useSWR<TxnResponse>(query, apiGet);

  async function onDelete(id: string) {
    try {
      await apiDelete(`/transactions/${id}`);
      
      // Invalidate all dependent caches to trigger refetch
      await invalidateTransactionData();
      
      toast({
        title: "Success!",
        description: "Transaction deleted successfully",
      });
    } catch (error) {
      toast({
        title: "Error",
        description: "Failed to delete transaction. Please try again.",
      });
    }
  }

  const getCategoryInfo = (categoryValue: string) => {
    return (
      categories.find((c) => c.value === categoryValue) || {
        label: categoryValue,
        color: "from-gray-500 to-slate-500",
      }
    );
  };

  const formatAmount = (amount: number, type: string) => {
    return formatCurrency(amount);
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString("en-US", {
      month: "short",
      day: "numeric",
      year: "numeric",
    });
  };

  return (
    <div className="space-y-6">
      {/* Filters */}
      <div className="bg-white/5 rounded-xl border border-white/10 p-4">
        <div className="flex flex-col sm:flex-row gap-4 items-stretch sm:items-center justify-between">
          <div className="flex flex-col sm:flex-row gap-3">
            <div className="flex items-center gap-2">
              <Filter className="h-4 w-4 text-[rgb(0,255,178)]" />
              <Select value={type} onValueChange={setType}>
                <SelectTrigger className="w-32 bg-white/5 border-white/20 text-white hover:bg-white/10">
                  <SelectValue placeholder="Type" />
                </SelectTrigger>
                <SelectContent className="bg-[rgb(8,7,14)] border-white/20">
                  <SelectItem
                    value="all"
                    className="text-white hover:bg-white/10"
                  >
                    All
                  </SelectItem>
                  <SelectItem
                    value="income"
                    className="text-white hover:bg-white/10"
                  >
                    Income
                  </SelectItem>
                  <SelectItem
                    value="expense"
                    className="text-white hover:bg-white/10"
                  >
                    Expense
                  </SelectItem>
                </SelectContent>
              </Select>
            </div>

            <Select value={category} onValueChange={setCategory}>
              <SelectTrigger className="w-40 bg-white/5 border-white/20 text-white hover:bg-white/10">
                <SelectValue placeholder="Category" />
              </SelectTrigger>
              <SelectContent className="bg-[rgb(8,7,14)] border-white/20">
                <SelectItem
                  value="all"
                  className="text-white hover:bg-white/10"
                >
                  All Categories
                </SelectItem>
                {categories.map((c) => (
                  <SelectItem
                    key={c.value}
                    value={c.value}
                    className="text-white hover:bg-white/10"
                  >
                    {c.label}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>

          <div className="flex items-center gap-2">
            <Search className="h-4 w-4 text-[rgb(0,255,178)]" />
            <Input
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              placeholder="Search transactions..."
              className="bg-white/5 border-white/20 text-white placeholder:text-white/50 hover:bg-white/10"
            />
          </div>
        </div>
      </div>

      {/* Table */}
      <div className="bg-white/5 rounded-xl border border-white/10 overflow-hidden">
        <div className="overflow-x-auto">
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead className="text-white/70 font-medium">
                  <div className="flex items-center gap-2">
                    <Calendar className="h-4 w-4" />
                    Date
                  </div>
                </TableHead>
                <TableHead className="text-white/70 font-medium">
                  <div className="flex items-center gap-2">
                    <FileText className="h-4 w-4" />
                    Description
                  </div>
                </TableHead>
                <TableHead className="text-white/70 font-medium">
                  <div className="flex items-center gap-2">
                    <Tag className="h-4 w-4" />
                    Type
                  </div>
                </TableHead>
                <TableHead className="text-white/70 font-medium">
                  Category
                </TableHead>
                <TableHead className="text-right text-white/70 font-medium">
                  <div className="flex items-center gap-2 justify-end">
                    <DollarSign className="h-4 w-4" />
                    Amount
                  </div>
                </TableHead>
                <TableHead className="text-white/70 font-medium">
                  Actions
                </TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {isLoading && (
                <TableRow>
                  <TableCell className="text-center text-white/60 py-8">
                    <div
                      className="flex items-center justify-center gap-2"
                      style={{ gridColumn: "1 / -1" }}
                    >
                      <div className="w-5 h-5 border-2 border-[rgb(0,255,178)]/30 border-t-[rgb(0,255,178)] rounded-full animate-spin"></div>
                      Loading transactions...
                    </div>
                  </TableCell>
                </TableRow>
              )}
              {data?.transactions?.map((t) => {
                const categoryInfo = getCategoryInfo(t.category || "");
                return (
                  <TableRow key={t.id}>
                    <TableCell className="text-white/90">
                      {formatDate(t.date)}
                    </TableCell>
                    <TableCell className="text-white/90">
                      {t.description || "—"}
                    </TableCell>
                    <TableCell>
                      <div
                        className={`flex items-center gap-2 ${
                          t.type === "income"
                            ? "text-[rgb(0,255,178)]"
                            : "text-red-400"
                        }`}
                      >
                        {t.type === "income" ? (
                          <TrendingUp className="h-4 w-4" />
                        ) : (
                          <TrendingDown className="h-4 w-4" />
                        )}
                        <span className="capitalize font-medium">{t.type}</span>
                      </div>
                    </TableCell>
                    <TableCell>
                      {t.category ? (
                        <span
                          className={`inline-flex items-center px-2 py-1 rounded-lg text-xs font-medium text-white`}
                        >
                          {categoryInfo.label}
                        </span>
                      ) : (
                        <span className="text-white/50">—</span>
                      )}
                    </TableCell>
                    <TableCell
                      className={`text-right font-mono font-semibold ${
                        t.type === "income"
                          ? "text-[rgb(0,255,178)]"
                          : "text-red-400"
                      }`}
                    >
                      {t.type === "expense" ? "-" : "+"}
                      {formatAmount(t.amount, t.type)}
                    </TableCell>
                    <TableCell>
                      <Button
                        variant="ghost"
                        size="sm"
                        onClick={() => onDelete(t.id)}
                        className="text-red-400 hover:text-red-300 hover:bg-red-500/10"
                      >
                        <Trash2 className="h-4 w-4" />
                      </Button>
                    </TableCell>
                  </TableRow>
                );
              })}
              {data && data.transactions.length === 0 && !isLoading && (
                <TableRow>
                  <TableCell className="text-center text-white/60 py-8">
                    No transactions found.
                  </TableCell>
                </TableRow>
              )}
            </TableBody>
          </Table>
        </div>
      </div>

      {/* Pagination */}
      <div className="flex items-center justify-between bg-white/5 rounded-xl border border-white/10 p-4">
        <div className="text-sm text-white/60">
          Page {data?.page ?? page} of {data?.total_pages ?? "—"} •{" "}
          {data?.total ?? 0} total transactions
        </div>
        <div className="flex gap-2">
          <Button
            variant="outline"
            size="sm"
            disabled={(data?.page ?? 1) <= 1}
            onClick={() => setPage((p) => Math.max(1, p - 1))}
            className="bg-white/5 border-white/20 text-white hover:bg-white/10"
          >
            Previous
          </Button>
          <Button
            variant="outline"
            size="sm"
            disabled={!!data && data.page >= data.total_pages}
            onClick={() => setPage((p) => p + 1)}
            className="bg-white/5 border-white/20 text-white hover:bg-white/10"
          >
            Next
          </Button>
        </div>
      </div>
    </div>
  );
}
