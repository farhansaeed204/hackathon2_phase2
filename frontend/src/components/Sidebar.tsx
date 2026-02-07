'use client';

import { Home, PlusCircle, Settings, User, LogOut } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { ScrollArea } from '@/components/ui/scroll-area';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { useRouter } from 'next/navigation';
import { logout } from '@/lib/api';

interface SidebarProps {
  isCollapsed?: boolean;
}

export function Sidebar({ isCollapsed = false }: SidebarProps) {
  const pathname = usePathname();

  const navItems = [
    {
      icon: Home,
      label: 'Dashboard',
      href: '/tasks',
      active: pathname === '/tasks' || pathname === '/'
    },
    {
      icon: Settings,
      label: 'Settings',
      href: '/settings',
      active: pathname === '/settings'
    },
    {
      icon: PlusCircle,
      label: 'New Task',
      href: '#',
      active: false
    }
  ];

  const router = useRouter();

  const handleLogout = async () => {
    try {
      await logout();
      router.push('/login');
      router.refresh();
    } catch (error) {
      console.error('Logout failed:', error);
    }
  };

  return (
    <div
      className={`h-full border-r flex flex-col ${
        isCollapsed ? 'w-16' : 'w-64'
      } transition-all duration-300`}
    >
      <div className="p-4 border-b">
        <h2 className={`text-xl font-bold text-center ${isCollapsed ? 'hidden' : 'block'}`}>
          TodoApp
        </h2>
      </div>

      <ScrollArea className="flex-1 py-2">
        <nav className="space-y-1 px-2">
          {navItems.map((item) => {
            const Icon = item.icon;
            return item.href === '#' ? (
              <button
                key="new-task"
                onClick={() => {
                  // This would trigger opening the task form modal
                  // In a real implementation, you would use a context or state management
                  // to open the modal from here
                  const event = new CustomEvent('openTaskModal');
                  window.dispatchEvent(event);
                }}
                className={`flex items-center gap-3 rounded-lg px-3 py-2 text-sm font-medium transition-colors w-full text-left hover:bg-accent hover:text-accent-foreground`}
              >
                <Icon className="h-5 w-5" />
                {!isCollapsed && <span>{item.label}</span>}
              </button>
            ) : (
              <Link
                key={item.href}
                href={item.href}
                className={`flex items-center gap-3 rounded-lg px-3 py-2 text-sm font-medium transition-colors ${
                  item.active
                    ? 'bg-accent text-accent-foreground'
                    : 'hover:bg-accent hover:text-accent-foreground'
                }`}
              >
                <Icon className="h-5 w-5" />
                {!isCollapsed && <span>{item.label}</span>}
              </Link>
            );
          })}
        </nav>
      </ScrollArea>

      <div className="p-4 border-t">
        <Button 
          variant="ghost" 
          className="w-full justify-start gap-3"
          onClick={handleLogout}
        >
          <LogOut className="h-5 w-5" />
          {!isCollapsed && <span>Logout</span>}
        </Button>
      </div>
    </div>
  );
}