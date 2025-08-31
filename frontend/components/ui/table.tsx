"use client"

import type * as React from "react"

import { cn } from "@/lib/utils"

export const Table = ({ children }: { children: React.ReactNode }) => (
  <div data-slot="table-container" className="relative w-full overflow-x-auto">
    <table data-slot="table" className="w-full caption-bottom text-sm">
      {children}
    </table>
  </div>
)

export const TableHeader = ({ children }: { children: React.ReactNode }) => (
  <thead data-slot="table-header" className="bg-gray-50 text-gray-600 [&_tr]:border-b">
    {children}
  </thead>
)

export const TableBody = ({ children }: { children: React.ReactNode }) => (
  <tbody data-slot="table-body" className="[&_tr:last-child]:border-0">
    {children}
  </tbody>
)

export const TableFooter = ({ className, ...props }: React.ComponentProps<"tfoot">) => {
  return (
    <tfoot
      data-slot="table-footer"
      className={cn("bg-muted/50 border-t font-medium [&>tr]:last:border-b-0", className)}
      {...props}
    />
  )
}

export const TableRow = ({ children }: { children: React.ReactNode }) => (
  <tr data-slot="table-row" className="hover:bg-muted/50 data-[state=selected]:bg-muted border-b transition-colors">
    {children}
  </tr>
)

export const TableHead = ({ children, className = "" }: { children: React.ReactNode; className?: string }) => (
  <th
    data-slot="table-head"
    className={cn(
      "text-foreground h-10 px-2 text-left align-middle font-medium whitespace-nowrap [&:has([role=checkbox])]:pr-0 [&>[role=checkbox]]:translate-y-[2px]",
      `bg-gray-50 text-gray-600 ${className}`,
    )}
  >
    {children}
  </th>
)

export const TableCell = ({ children, className = "" }: { children: React.ReactNode; className?: string }) => (
  <td
    data-slot="table-cell"
    className={cn(
      "p-2 align-middle whitespace-nowrap [&:has([role=checkbox])]:pr-0 [&>[role=checkbox]]:translate-y-[2px]",
      className,
    )}
  >
    {children}
  </td>
)

function TableCaption({ className, ...props }: React.ComponentProps<"caption">) {
  return (
    <caption data-slot="table-caption" className={cn("text-muted-foreground mt-4 text-sm", className)} {...props} />
  )
}

export { TableCaption }
