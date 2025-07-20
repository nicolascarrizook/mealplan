import * as React from "react"
import { cn } from "@/lib/utils"

interface RangeSliderProps extends Omit<React.InputHTMLAttributes<HTMLInputElement>, 'type'> {
  showValue?: boolean
  suffix?: string
}

export const RangeSlider = React.forwardRef<HTMLInputElement, RangeSliderProps>(
  ({ className, showValue = true, suffix = "", value, ...props }, ref) => {
    return (
      <div className="w-full space-y-2">
        <div className="relative">
          <input
            type="range"
            ref={ref}
            value={value}
            className={cn(
              "w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer",
              "focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary",
              "[&::-webkit-slider-thumb]:appearance-none",
              "[&::-webkit-slider-thumb]:w-5",
              "[&::-webkit-slider-thumb]:h-5",
              "[&::-webkit-slider-thumb]:rounded-full",
              "[&::-webkit-slider-thumb]:bg-primary",
              "[&::-webkit-slider-thumb]:cursor-pointer",
              "[&::-webkit-slider-thumb]:transition-all",
              "[&::-webkit-slider-thumb]:hover:scale-110",
              "[&::-moz-range-thumb]:w-5",
              "[&::-moz-range-thumb]:h-5",
              "[&::-moz-range-thumb]:rounded-full",
              "[&::-moz-range-thumb]:bg-primary",
              "[&::-moz-range-thumb]:border-0",
              "[&::-moz-range-thumb]:cursor-pointer",
              "[&::-moz-range-thumb]:transition-all",
              "[&::-moz-range-thumb]:hover:scale-110",
              className
            )}
            {...props}
          />
        </div>
        {showValue && (
          <div className="text-sm text-muted-foreground text-center">
            {value}{suffix}
          </div>
        )}
      </div>
    )
  }
)

RangeSlider.displayName = "RangeSlider"