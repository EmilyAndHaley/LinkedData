# opens the orpha epidemiological data

require 'net/http'
require 'rexml/document'
require 'nokogiri'
require 'xapian'

load 'levenshtein_distance.rb'

file = File.read("../../Dictionaries/Orphadata/EpidemiologicalData/en_product2.xml")
xml = Nokogiri::XML(file)

bestmatchnum=500
match='nothing'

# Open the database for update, creating a new database if necessary.
xml.xpath("//Disorder/Name").each do |node|
	
	matchnum=levenshtein_distance(node.content, ARGV[0])
	puts node.content+':'+matchnum.to_s+' '+bestmatchnum.to_s
	if matchnum<bestmatchnum
		match=node.content
		bestmatchnum=matchnum
	end
#node.content = node.content.gsub(/\n\s+/, " ")
end

puts 'best match is: '+match
