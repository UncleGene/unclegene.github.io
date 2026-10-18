ActiveRecord::Schema.define do
  drop_table :records if table_exists? :records
  create_table :records do |t|
    t.timestamps
  end
end

class Record < ActiveRecord::Base
end

class CuriousFirstTest < MiniTest::Unit::TestCase
  def test_first_last
    r = Record.create
    Record.create
    r.touch
    assert_equal 2, Record.count
    assert Record.first != Record.last, 'The first of 2 records is also the last!'
  end
end
