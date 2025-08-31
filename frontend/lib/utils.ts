import { clsx, type ClassValue } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

/**
 * Format amount as Indian Rupees currency
 * @param amount - The amount to format
 * @param showSymbol - Whether to show the ₹ symbol (default: true)
 * @returns Formatted currency string
 */
export function formatCurrency(amount: number, showSymbol: boolean = true): string {
  const formatted = new Intl.NumberFormat("en-IN", {
    style: "currency",
    currency: "INR",
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  }).format(amount)
  
  // If showSymbol is false, remove the ₹ symbol and return just the number
  if (!showSymbol) {
    return formatted.replace(/₹\s?/, '')
  }
  
  return formatted
}

/**
 * Format amount as compact Indian Rupees (e.g., ₹1.2L, ₹5.5K)
 * @param amount - The amount to format
 * @returns Compact currency string
 */
export function formatCompactCurrency(amount: number): string {
  if (amount >= 10000000) { // 1 Crore
    return `₹${(amount / 10000000).toFixed(1)}Cr`
  } else if (amount >= 100000) { // 1 Lakh
    return `₹${(amount / 100000).toFixed(1)}L`
  } else if (amount >= 1000) { // 1 Thousand
    return `₹${(amount / 1000).toFixed(1)}K`
  } else {
    return formatCurrency(amount)
  }
}
