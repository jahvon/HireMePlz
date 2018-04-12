require "json"
require "selenium-webdriver"
require "rspec"
include RSpec::Expectations

describe "LoginIncorrectPassword" do

  before(:each) do
    @driver = Selenium::WebDriver.for :firefox
    @base_url = "https://www.katalon.com/"
    @accept_next_alert = true
    @driver.manage.timeouts.implicit_wait = 30
    @verification_errors = []
  end
  
  after(:each) do
    @driver.quit
    @verification_errors.should == []
  end
  
  it "test_login_incorrect_password" do
    @driver.get "http://127.0.0.1:5000/login"
    @driver.find_element(:id, "staticEmail").click
    @driver.find_element(:id, "staticEmail").clear
    @driver.find_element(:id, "staticEmail").send_keys "jahvon_dockerty@gmail.com"
    @driver.find_element(:id, "inputPassword").clear
    @driver.find_element(:id, "inputPassword").send_keys "blahblahblah"
    @driver.find_element(:xpath, "//button[@type='submit']").click
  end
  
  def element_present?(how, what)
    ${receiver}.find_element(how, what)
    true
  rescue Selenium::WebDriver::Error::NoSuchElementError
    false
  end
  
  def alert_present?()
    ${receiver}.switch_to.alert
    true
  rescue Selenium::WebDriver::Error::NoAlertPresentError
    false
  end
  
  def verify(&blk)
    yield
  rescue ExpectationNotMetError => ex
    @verification_errors << ex
  end
  
  def close_alert_and_get_its_text(how, what)
    alert = ${receiver}.switch_to().alert()
    alert_text = alert.text
    if (@accept_next_alert) then
      alert.accept()
    else
      alert.dismiss()
    end
    alert_text
  ensure
    @accept_next_alert = true
  end
end
