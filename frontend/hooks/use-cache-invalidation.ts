import { mutate } from 'swr'

/**
 * Custom hook for centralizing SWR cache invalidation patterns
 * This ensures consistent data refetching across the application
 */
export function useCacheInvalidation() {
  
  /**
   * Invalidate all transaction-related data
   * Call this after creating, updating, or deleting transactions
   */
  const invalidateTransactionData = async () => {
    return Promise.all([
      // Invalidate transactions data (all pages and filters)
      mutate(key => typeof key === 'string' && key.startsWith('/transactions')),
      // Invalidate analytics data
      mutate('/analytics/daily-budget'),
      mutate('/analytics/daily-report'),
      mutate('/analytics/monthly-report'),
      mutate('/analytics/category-breakdown'),
      mutate('/analytics/goal-progress'),
      // Invalidate goals data (as transactions affect progress)
      mutate('/goals'),
      // Invalidate user profile data (current_amount changes)
      mutate('/user/profile'),
    ])
  }

  /**
   * Invalidate all goal-related data
   * Call this after creating, updating, or deleting goals
   */
  const invalidateGoalData = async () => {
    return Promise.all([
      // Invalidate goals data
      mutate('/goals'),
      // Invalidate analytics data (goals affect budget calculations)
      mutate('/analytics/daily-budget'),
      mutate('/analytics/goal-progress'),
      // Invalidate daily report (may include goal-related insights)
      mutate('/analytics/daily-report'),
    ])
  }

  /**
   * Invalidate all analytics data
   * Call this when you need to refresh all analytics/reports
   */
  const invalidateAnalyticsData = async () => {
    return Promise.all([
      mutate('/analytics/daily-budget'),
      mutate('/analytics/daily-report'),
      mutate('/analytics/monthly-report'),
      mutate('/analytics/category-breakdown'),
      mutate('/analytics/goal-progress'),
    ])
  }

  /**
   * Invalidate user profile data
   * Call this after updating user settings or when balance changes
   */
  const invalidateUserData = async () => {
    return Promise.all([
      mutate('/user/profile'),
      // Also invalidate budget as it depends on user settings
      mutate('/analytics/daily-budget'),
    ])
  }

  /**
   * Nuclear option: invalidate everything
   * Use sparingly, mainly for login/logout or major data changes
   */
  const invalidateAllData = async () => {
    return Promise.all([
      mutate(key => typeof key === 'string' && key.startsWith('/transactions')),
      mutate(key => typeof key === 'string' && key.startsWith('/analytics')),
      mutate('/goals'),
      mutate('/user/profile'),
    ])
  }

  return {
    invalidateTransactionData,
    invalidateGoalData,
    invalidateAnalyticsData,
    invalidateUserData,
    invalidateAllData,
  }
}
