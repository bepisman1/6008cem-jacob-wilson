class VCardParser:
    def __init__(self):
        self.vcards = []

    def parse_vcard_file(self, file_path):
        self.vcards = []  # Clear existing vCards
        with open(file_path, 'r') as file:
            lines = file.readlines()
            self.parse_vcard_lines(lines)

    def parse_vcard_lines(self, lines):
        vcard_lines = []
        for line in lines:
            if line.strip():  # Skip empty lines
                vcard_lines.append(line.strip())
            elif vcard_lines:
                self.parse_vcard_properties(vcard_lines)
                vcard_lines = []

        if vcard_lines:  # Parse last vCard if there are remaining lines
            self.parse_vcard_properties(vcard_lines)

    def parse_vcard_properties(self, lines):
        vcard = {}
        for line in lines:
            name, value = line.split(':', 1)
            vcard[name] = value.strip()
        self.vcards.append(vcard)

    def vcard_to_html(self):
        html = ''
        for vcard in self.vcards:
            html += '<div class="vcard">'
            for name, value in vcard.items():
                html += f'<div><span class="property-name">{name}:</span> <span class="property-value">{value}</span></div>'
            html += '</div>'
        return html


# Example usage:
parser = VCardParser()
parser.parse_vcard_file("D:\Downlaods\Simon Perreault's homepage_files")
html = parser.vcard_to_html()
print(html)
