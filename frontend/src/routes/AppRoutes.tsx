import { Navigate, Route, Routes } from 'react-router-dom'
import { AppLayout } from '../layouts/AppLayout'
import { RequireAuth, RequireRole } from '../components/RequireAuth'
import { LoginPage } from '../pages/LoginPage'
import { UnauthorizedPage } from '../pages/UnauthorizedPage'
import { AdminDashboard } from '../pages/admin/AdminDashboard'
import { StaffDashboard } from '../pages/staff/StaffDashboard'
import { StudentDashboard } from '../pages/student/StudentDashboard'
import { StudentsPage } from '../pages/admin/StudentsPage'
import { ApplicationsPage } from '../pages/admin/ApplicationsPage'
import { RoomsPage } from '../pages/admin/RoomsPage'
import { NoticesPage } from '../pages/admin/NoticesPage'
import { MyRoomPage } from '../pages/student/MyRoomPage'
import { PaymentsPage } from '../pages/student/PaymentsPage'

export function AppRoutes() {
  return (
    <Routes>
      <Route path="/login" element={<LoginPage />} />
      <Route path="/unauthorized" element={<UnauthorizedPage />} />

      <Route element={<RequireAuth />}>
        <Route element={<AppLayout />}>
          <Route
            path="/admin"
            element={
              <RequireRole roles={['ADMIN']}>
                <AdminDashboard />
              </RequireRole>
            }
          />
          <Route
            path="/admin/students"
            element={
              <RequireRole roles={['ADMIN']}>
                <StudentsPage />
              </RequireRole>
            }
          />
          <Route
            path="/admin/applications"
            element={
              <RequireRole roles={['ADMIN']}>
                <ApplicationsPage />
              </RequireRole>
            }
          />
          <Route
            path="/admin/rooms"
            element={
              <RequireRole roles={['ADMIN']}>
                <RoomsPage />
              </RequireRole>
            }
          />
          <Route
            path="/admin/notices"
            element={
              <RequireRole roles={['ADMIN']}>
                <NoticesPage />
              </RequireRole>
            }
          />
          <Route
            path="/staff"
            element={
              <RequireRole roles={['STAFF']}>
                <StaffDashboard />
              </RequireRole>
            }
          />
          <Route
            path="/student"
            element={
              <RequireRole roles={['STUDENT']}>
                <StudentDashboard />
              </RequireRole>
            }
          />
          <Route
            path="/student/my-room"
            element={
              <RequireRole roles={['STUDENT']}>
                <MyRoomPage />
              </RequireRole>
            }
          />
          <Route
            path="/student/payments"
            element={
              <RequireRole roles={['STUDENT']}>
                <PaymentsPage />
              </RequireRole>
            }
          />
        </Route>
      </Route>

      <Route path="/" element={<Navigate to="/login" replace />} />
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  )
}
