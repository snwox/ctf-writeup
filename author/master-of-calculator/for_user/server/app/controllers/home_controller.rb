class HomeController < ApplicationController
  skip_forgery_protection :only => [:calculate_fee]
  FILTER = ["system", "eval", "exec", "Dir", "File", "IO", "require", "fork", "spawn", "syscall", '"', "'", "(", ")", "[", "]","{","}", "`", "%","<",">"]

  def index
    render :home
  end

  def calculate_fee
      entry_price = params[:user_entry_price]
      exit_price = params[:user_exit_price]
      leverage = params[:user_leverage].to_f
      quantity = params[:user_quantity]

      if [entry_price, exit_price, leverage, quantity].map(&:to_s).any? { |input| FILTER.any? { |word| input.include?(word) } }
        response = "filtered"
      else
          response = ERB.new(<<~FORMULA
          <% pnl = ((#{exit_price} - #{entry_price}) * #{quantity} * #{leverage}).round(3) %>
          <% roi = (((#{exit_price} - #{entry_price}) * 100.0 / #{entry_price} * #{leverage})).round(3) %>
          <% initial_margin = ((#{entry_price} * #{quantity}) / #{leverage}).round(3) %>
          <%= pnl %>
          <%= roi %>%
          <%= initial_margin %>
          FORMULA
          ).result(binding)
          response = response.sub("\n\n\n","")
          pnl, roi, margin = response.split("\n")
      end
  
      render json: { response: response, pnl: pnl, roi: roi, margin: margin }

    end
end