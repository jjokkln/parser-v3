from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm, cm
import io
import os

class ProfileGenerator:
    """Klasse zur Erstellung von PDF-Profilen aus strukturierten Daten"""
    
    def __init__(self):
        """Initialisiert den Profil-Generator mit Stilen"""
        self.styles = getSampleStyleSheet()
        self.custom_styles = self._create_custom_styles()
    
    def generate_profile(self, profile_data, output_path):
        """
        Generiert ein PDF-Profil aus den extrahierten Daten
        
        Args:
            profile_data: Dictionary mit Profildaten
            output_path: Pfad für die Ausgabedatei
        
        Returns:
            Pfad zur generierten PDF-Datei
        """
        # Erstelle das PDF-Dokument
        doc = SimpleDocTemplate(
            output_path,
            pagesize=A4,
            rightMargin=20*mm, 
            leftMargin=20*mm,
            topMargin=20*mm, 
            bottomMargin=20*mm
        )
        
        # Erstelle die Dokumentelemente
        elements = self._create_document_elements(profile_data)
        
        # Erstelle das PDF
        doc.build(elements)
        
        return output_path
    
    def _create_custom_styles(self):
        """Erstellt benutzerdefinierte Stile für das Dokument"""
        custom_styles = {}
        
        # Haupttitel
        custom_styles['Title'] = ParagraphStyle(
            'Title',
            parent=self.styles['Title'],
            fontSize=16,
            textColor=colors.darkblue,
            spaceAfter=0.5*cm
        )
        
        # Überschrift für Abschnitte
        custom_styles['Heading2'] = ParagraphStyle(
            'Heading2',
            parent=self.styles['Heading2'],
            fontSize=12,
            textColor=colors.darkblue,
            spaceAfter=0.3*cm,
            spaceBefore=0.6*cm
        )
        
        # Normaler Text
        custom_styles['Normal'] = ParagraphStyle(
            'Normal',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceAfter=0.2*cm
        )
        
        # Firmenname/Position - Hervorgehoben
        custom_styles['Company'] = ParagraphStyle(
            'Company',
            parent=self.styles['Normal'],
            fontSize=10,
            fontName='Helvetica-Bold',
            spaceAfter=0.1*cm
        )
        
        # Zeitraum - Kleiner und grau
        custom_styles['Period'] = ParagraphStyle(
            'Period',
            parent=self.styles['Normal'],
            fontSize=9,
            textColor=colors.darkgrey
        )
        
        return custom_styles
    
    def _create_document_elements(self, profile_data):
        """Erstellt die Elemente für das PDF-Dokument"""
        elements = []
        
        # Persönliche Daten
        personal_data = profile_data.get('persönliche_daten', {})
        
        # Name als Haupttitel
        name = personal_data.get('name', 'Profil')
        elements.append(Paragraph(f"Profil<br/>{name}", self.custom_styles['Title']))
        elements.append(Spacer(1, 0.2*cm))
        
        # Kontaktinformationen
        kontakt = personal_data.get('kontakt', {})
        contact_table_data = [
            ['Ansprechpartner:', kontakt.get('ansprechpartner', '')],
            ['Telefon:', kontakt.get('telefon', '')],
            ['E-Mail:', kontakt.get('email', '')]
        ]
        
        # Persönliche Informationen
        personal_table_data = [
            ['Wohnort:', personal_data.get('wohnort', '')],
            ['Jahrgang:', personal_data.get('jahrgang', '')],
            ['Führerschein:', personal_data.get('führerschein', '')]
        ]
        
        # Tabelle für Kontakt und persönliche Infos
        info_table = Table(contact_table_data + [['', '']] + personal_table_data, colWidths=[100, 380])
        info_table.setStyle(TableStyle([
            ('FONT', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONT', (1, 0), (1, -1), 'Helvetica'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
            ('TOPPADDING', (0, 0), (-1, -1), 5),
        ]))
        
        elements.append(info_table)
        elements.append(Spacer(1, 0.5*cm))
        
        # Linie nach persönlichen Daten
        elements.append(self._create_horizontal_line())
        
        # Beruflicher Werdegang
        elements.append(Paragraph("Beruflicher Werdegang", self.custom_styles['Heading2']))
        
        # Berufserfahrungen hinzufügen
        for erfahrung in profile_data.get('berufserfahrung', []):
            # Zeitraum
            elements.append(Paragraph(erfahrung.get('zeitraum', ''), self.custom_styles['Period']))
            
            # Unternehmen und Position
            elements.append(Paragraph(
                f"{erfahrung.get('unternehmen', '')}<br/>{erfahrung.get('position', '')}",
                self.custom_styles['Company']
            ))
            
            # Aufgaben als Aufzählung
            for aufgabe in erfahrung.get('aufgaben', []):
                elements.append(Paragraph(f"• {aufgabe}", self.custom_styles['Normal']))
            
            elements.append(Spacer(1, 0.3*cm))
        
        # Ausbildung
        elements.append(Paragraph("Ausbildung/ Weiterbildung", self.custom_styles['Heading2']))
        
        # Ausbildungen hinzufügen
        for ausbildung in profile_data.get('ausbildung', []):
            # Zeitraum
            elements.append(Paragraph(ausbildung.get('zeitraum', ''), self.custom_styles['Period']))
            
            # Institution und Abschluss
            elements.append(Paragraph(
                f"{ausbildung.get('institution', '')}<br/>"
                f"{ausbildung.get('abschluss', '')}",
                self.custom_styles['Company']
            ))
            
            # Note wenn vorhanden
            if ausbildung.get('note'):
                elements.append(Paragraph(f"Abschlussnote {ausbildung.get('note')}", self.custom_styles['Normal']))
            
            elements.append(Spacer(1, 0.3*cm))
        
        # Weiterbildungen hinzufügen
        for weiterbildung in profile_data.get('weiterbildungen', []):
            # Zeitraum
            elements.append(Paragraph(weiterbildung.get('zeitraum', ''), self.custom_styles['Period']))
            
            # Bezeichnung und Abschluss
            bezeichnung = weiterbildung.get('bezeichnung', '')
            abschluss = weiterbildung.get('abschluss', '')
            
            if abschluss:
                elements.append(Paragraph(
                    f"{bezeichnung}<br/>Abschluss: {abschluss}",
                    self.custom_styles['Company']
                ))
            else:
                elements.append(Paragraph(bezeichnung, self.custom_styles['Company']))
            
            elements.append(Spacer(1, 0.3*cm))
        
        # Optional: Firmenfußzeile hinzufügen
        elements.append(Spacer(1, 1*cm))
        elements.append(self._create_footer())
        
        return elements
    
    def _create_horizontal_line(self):
        """Erstellt eine horizontale Linie als Tabelle"""
        table_data = [['']]
        line = Table(table_data, colWidths=[480], rowHeights=[1])
        line.setStyle(TableStyle([
            ('LINEABOVE', (0, 0), (-1, -1), 1, colors.darkblue),
        ]))
        return line
    
    def _create_footer(self):
        """Erstellt eine Fußzeile"""
        footer_text = "GALDORA Personalmanagement GmbH Co.KG<br/>"
        footer_text += "Volksgartenstr. 85-89, 41065 Mönchengladbach<br/>"
        footer_text += "E-Mail: info@galdora.de / Web: www.galdora.de"
        
        footer_style = ParagraphStyle(
            'Footer',
            parent=self.styles['Normal'],
            fontSize=8,
            textColor=colors.darkgrey,
            alignment=1  # Zentriert
        )
        
        return Paragraph(footer_text, footer_style)
