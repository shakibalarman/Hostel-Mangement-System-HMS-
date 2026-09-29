import { api } from './client'

export interface MealStats {
  current_month_meals: number
  last_month_meals: number
  total_meals: number
  balance: number
  total_spent: number
  daily_average: number
}

export interface MealBalance {
  id: number
  student_id: number
  total_meals_purchased: number
  meals_consumed: number
  balance: number
  last_updated: string
}

export interface MealRecord {
  id: number
  student_id: number
  meal_date: string
  meal_type: string
  quantity: number
  cost_per_meal: number
  notes: string | null
  created_at: string
}

export const mealTrackingApi = {
  getStats: () => api.get<MealStats>('/meal-tracking/stats').then((r) => r.data),
  getBalance: () => api.get<MealBalance>('/meal-tracking/balance').then((r) => r.data),
  getMeals: (params?: { month?: number; year?: number }) =>
    api.get<MealRecord[]>('/meal-tracking/meals', { params }).then((r) => r.data),
  recordMeal: (data: { meal_date: string; meal_type: string; quantity: number; cost_per_meal: number; notes?: string }) =>
    api.post<MealRecord>('/meal-tracking/meals', data).then((r) => r.data),
  purchaseMeals: (quantity: number) =>
    api.post<MealBalance>('/meal-tracking/purchase', null, { params: { quantity } }).then((r) => r.data),
}
