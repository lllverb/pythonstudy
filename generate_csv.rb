require 'fileutils'

train_data_path = "./data/train/data.txt"
test_data_path = "./data/test/data.txt"

FileUtils.touch(train_data_path) unless FileTest.exist?(train_data_path)
FileUtils.touch(test_data_path) unless FileTest.exist?(test_data_path)


test_chiba_data_paths = Dir.glob("./data/test/chiba/*.jpg")
test_daiki_data_paths = Dir.glob("./data/test/daiki/*.jpg")
test_sakurai_data_paths = Dir.glob("./data/test/sakurai/*.jpg")
train_chiba_data_paths = Dir.glob("./data/train/chiba/*.jpg")
train_daiki_data_paths = Dir.glob("./data/train/daiki/*.jpg")
train_sakurai_data_paths = Dir.glob("./data/train/sakurai/*.jpg")


File.open(test_data_path, "w") do |f|
  test_chiba_data_paths.each { |path| f.puts("#{path} 0") }
  test_daiki_data_paths.each { |path| f.puts("#{path} 1") }
  test_sakurai_data_paths.each { |path| f.puts("#{path} 2") }
end
File.open(train_data_path, "w") do |f|
  train_chiba_data_paths.each { |path| f.puts("#{path} 0") }
  train_daiki_data_paths.each { |path| f.puts("#{path} 1") }
  train_sakurai_data_paths.each { |path| f.puts("#{path} 2") }
end