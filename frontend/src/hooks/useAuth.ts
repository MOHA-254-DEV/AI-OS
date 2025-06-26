import { useAuth } from "../context/AuthContext";

export function useLogin() {
  const { login, loading } = useAuth();
  return { login, loading };
}

export function useLogout() {
  const { logout, loading } = useAuth();
  return { logout, loading };
}

export function useCurrentUser() {
  const { user, loading } = useAuth();
  return { user, loading };
}
