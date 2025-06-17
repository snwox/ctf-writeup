Rails.application.routes.draw do
  root "home#index"
  post 'calculate_fee' => 'home#calculate_fee'
end
