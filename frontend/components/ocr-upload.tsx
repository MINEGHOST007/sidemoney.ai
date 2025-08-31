"use client"

import { useState } from "react"
import { apiPost } from "@/lib/api"
import { formatCurrency } from "@/lib/utils"
import { useCacheInvalidation } from "@/hooks/use-cache-invalidation"
import { Button } from "@/components/ui/button"

type OcrTxn = {
  description: string
  amount: number
  date: string
  category?: string
  confidence: number
}

export function OcrUpload() {
  const [file, setFile] = useState<File | null>(null)
  const [results, setResults] = useState<OcrTxn[]>([])
  const [isLoading, setIsLoading] = useState(false)
  const { invalidateTransactionData } = useCacheInvalidation()

  async function onUpload() {
    if (!file) return
    setIsLoading(true)
    try {
      const form = new FormData()
      form.append("file", file)
      const res = await fetch("/ai/ocr/process", {
        method: "POST",
        body: form,
        headers: {
          // Authorization header will be set via reverse proxy? Instead, call absolute API:
        },
      })
      // The above won't include auth; instead call backend directly using apiPost with FormData
    } catch {}
    try {
      const form = new FormData()
      form.append("file", file)
      const data = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000"}/ai/ocr/process`, {
        method: "POST",
        body: form,
        headers: {
          Authorization: `Bearer ${localStorage.getItem("access_token") || ""}`,
        },
      }).then((r) => r.json())
      setResults(data.transactions || [])
    } catch (e: any) {
      alert(e?.message || "Upload failed")
    } finally {
      setIsLoading(false)
    }
  }

  async function saveAll() {
    if (!results.length) return
    try {
      await apiPost("/transactions/bulk", {
        transactions: results,
        source: "ocr",
        verify_before_save: true,
      })
      
      // Invalidate all dependent caches to trigger refetch
      await invalidateTransactionData()
      
      alert("Transactions created")
      setResults([])
    } catch (e: any) {
      alert(e?.message || "Bulk create failed")
    }
  }

  return (
    <div className="rounded-2xl border border-white/10 bg-white/5 p-6">
      <div className="flex flex-col sm:flex-row items-start sm:items-center gap-4">
        <div className="flex-1">
          <input 
            type="file" 
            accept="image/*" 
            onChange={(e) => setFile(e.target.files?.[0] || null)}
            className="block w-full text-sm text-white/70 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-semibold file:bg-[rgb(0,255,178)] file:text-black hover:file:bg-[rgb(0,255,178)]/90 file:transition-colors"
          />
        </div>
        <div className="flex gap-2">
          <Button 
            onClick={onUpload} 
            disabled={!file || isLoading} 
            className="bg-[rgb(0,255,178)] text-black hover:bg-[rgb(0,255,178)]/90 font-semibold"
          >
            {isLoading ? "Processing..." : "Process OCR"}
          </Button>
          <Button 
            variant="outline" 
            onClick={saveAll} 
            disabled={!results.length}
            className="border-white/20 text-white hover:bg-white/10"
          >
            Save All
          </Button>
        </div>
      </div>
      {results.length > 0 && (
        <div className="mt-6">
          <h4 className="font-semibold text-white mb-4 flex items-center gap-2">
            <div className="w-2 h-2 rounded-full bg-[rgb(0,255,178)]" />
            Detected Transactions
          </h4>
          <div className="space-y-3">
            {results.map((t, i) => (
              <div key={i} className="bg-white/5 rounded-xl border border-white/10 p-4 hover:bg-white/10 transition-colors">
                <div className="flex items-center justify-between">
                  <div className="flex-1">
                    <div className="font-medium text-white mb-1">{t.description}</div>
                    <div className="text-sm text-white/60 flex items-center gap-3">
                      <span className="font-semibold text-[rgb(0,255,178)]">{formatCurrency(Number(t.amount))}</span>
                      <span>•</span>
                      <span>{t.date}</span>
                      <span>•</span>
                      <span className="px-2 py-1 rounded-md bg-white/10 text-xs">{t.category || "Uncategorized"}</span>
                      <span>•</span>
                      <span className="text-xs">
                        {Math.round((t.confidence || 0) * 100)}% confidence
                      </span>
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}
