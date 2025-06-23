"use client";

import { cn } from "@/utils/cn";
import { usePathname } from "next/navigation";
import { ReactNode } from "react";
import Link from "next/link";

export const ActiveLink = (props) => {
  const pathname = usePathname();
  return (
    <Link
      href={props.href}
      className={cn(
        "px-4 py-2 rounded-[18px] whitespace-nowrap flex items-center gap-2 text-sm transition-all",
        pathname === props.href && "bg-primary text-primary-foreground",
      )}
    >
      {props.children}
    </Link>
  );
};


