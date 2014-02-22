require 'net/http'
require 'rexml/document'
require 'nokogiri'
require 'xapian'

file = File.read("../../Dictionaries/Orphadata/EpidemiologicalData/en_product2.xml")
xml = Nokogiri::XML(file)

# Open the database for update, creating a new database if necessary.
database = Xapian::WritableDatabase.new(ARGV[0], Xapian::DB_CREATE_OR_OPEN)

indexer = Xapian::TermGenerator.new()
stemmer = Xapian::Stem.new("english")
indexer.database=database
indexer.stemmer = stemmer

xml.xpath("//Disorder/Name").each do |node|
	puts node.content  

	  doc = Xapian::Document.new()
      doc.data = node.content

      indexer.document = doc
      indexer.index_text(node.content)
	  indexer.set_flags(Xapian::TermGenerator::FLAG_SPELLING)

      # Add the document to the database
      database.add_document(doc)
	
#node.content = node.content.gsub(/\n\s+/, " ")
end
