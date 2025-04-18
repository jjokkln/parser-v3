from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm, cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
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
        
        # GALDORA Überschrift-Stil (große schwarze Schrift)
        custom_styles['GaldoraLogo'] = ParagraphStyle(
            'GaldoraLogo',
            parent=self.styles['Normal'],
            fontSize=36,
            fontName='Helvetica-Bold',
            textColor=colors.black,
            spaceAfter=0.1*cm
        )

        # Tagline unter dem Logo
        custom_styles['Tagline'] = ParagraphStyle(
            'Tagline',
            parent=self.styles['Italic'],
            fontSize=10,
            fontName='Helvetica-Oblique',
            textColor=colors.black,
            spaceAfter=1.5*cm
        )
        
        # Profil Überschrift
        custom_styles['ProfilTitle'] = ParagraphStyle(
            'ProfilTitle',
            parent=self.styles['Heading1'],
            fontSize=18,
            fontName='Helvetica-Bold',
            textColor=colors.darkblue,
            spaceBefore=0.5*cm,
            spaceAfter=0.2*cm
        )
        
        # Name
        custom_styles['Name'] = ParagraphStyle(
            'Name',
            parent=self.styles['Normal'],
            fontSize=16,
            fontName='Helvetica',
            spaceBefore=0.2*cm,
            spaceAfter=1.5*cm
        )
        
        # Überschrift für Abschnitte
        custom_styles['Heading2'] = ParagraphStyle(
            'Heading2',
            parent=self.styles['Heading2'],
            fontSize=14,
            fontName='Helvetica-Bold',
            textColor=colors.black,
            spaceBefore=0.6*cm,
            spaceAfter=0.3*cm
        )
        
        # Ansprechpartner Überschrift
        custom_styles['ContactHeader'] = ParagraphStyle(
            'ContactHeader',
            parent=self.styles['Normal'],
            fontSize=10,
            fontName='Helvetica-Bold',
            spaceBefore=0.2*cm,
            spaceAfter=0.1*cm
        )
        
        # Normaler Text
        custom_styles['Normal'] = ParagraphStyle(
            'Normal',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceAfter=0.2*cm
        )
        
        # Label-Text (fett)
        custom_styles['Label'] = ParagraphStyle(
            'Label',
            parent=self.styles['Normal'],
            fontSize=10,
            fontName='Helvetica-Bold',
            spaceAfter=0.1*cm
        )
        
        # Firmenname - Hervorgehoben
        custom_styles['Company'] = ParagraphStyle(
            'Company',
            parent=self.styles['Normal'],
            fontSize=10,
            fontName='Helvetica-Bold',
            spaceAfter=0.1*cm
        )
        
        # Position/Rolle - Kursiv
        custom_styles['Position'] = ParagraphStyle(
            'Position',
            parent=self.styles['Italic'],
            fontSize=10,
            fontName='Helvetica-Oblique',
            spaceAfter=0.2*cm
        )
        
        # Zeitraum
        custom_styles['Period'] = ParagraphStyle(
            'Period',
            parent=self.styles['Normal'],
            fontSize=10,
            fontName='Helvetica-Bold',
            spaceAfter=0.1*cm
        )
        
        return custom_styles
    
    def _create_document_elements(self, profile_data):
        """Erstellt die Elemente für das PDF-Dokument"""
        elements = []
        
        # GALDORA Logo und Tagline
        elements.append(Paragraph("GALDORA", self.custom_styles['GaldoraLogo']))
        elements.append(Paragraph("Ich ist, was wir tun", self.custom_styles['Tagline']))
        
        # Profil Überschrift
        elements.append(Paragraph("Profil", self.custom_styles['ProfilTitle']))
        
        # Persönliche Daten
        personal_data = profile_data.get('persönliche_daten', {})
        
        # Name
        name = personal_data.get('name', 'Profil')
        elements.append(Paragraph(name, self.custom_styles['Name']))
        
        # Ansprechpartner Block
        elements.append(Paragraph("IHR ANSPRECHPARTNER", self.custom_styles['ContactHeader']))
        
        # Kontaktinformationen
        kontakt = personal_data.get('kontakt', {})
        ansprechpartner = kontakt.get('ansprechpartner', 'Herr Fischer')
        telefon = kontakt.get('telefon', '02161 62126-02')
        email = kontakt.get('email', 'fischer@galdora.de')
        
        contact_data = [
            [Paragraph(f"Herr {ansprechpartner}", self.custom_styles['Normal'])],
            [Paragraph(f"Telefon: {telefon}", self.custom_styles['Normal'])],
            [Paragraph(f"E-Mail: {email}", self.custom_styles['Normal'])]
        ]
        
        contact_table = Table(contact_data, colWidths=[450])
        contact_table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
            ('TOPPADDING', (0, 0), (-1, -1), 3),
        ]))
        
        elements.append(contact_table)
        elements.append(Spacer(1, 1*cm))
        
        # Horizontale Linie
        elements.append(HRFlowable(width="100%", thickness=1, color=colors.lightgrey, spaceAfter=0.5*cm))
        
        # Persönliche Informationen
        wohnort = personal_data.get('wohnort', '')
        jahrgang = personal_data.get('jahrgang', '')
        führerschein = personal_data.get('führerschein', 'Klasse B (Pkw vorhanden)')
        
        # Persönliche Daten als separate Zeilen mit Labels
        elements.append(Paragraph("Wohnort:", self.custom_styles['Label']))
        elements.append(Paragraph(wohnort, self.custom_styles['Normal']))
        
        elements.append(Paragraph("Jahrgang:", self.custom_styles['Label']))
        elements.append(Paragraph(jahrgang, self.custom_styles['Normal']))
        
        elements.append(Paragraph("Führerschein:", self.custom_styles['Label']))
        elements.append(Paragraph(führerschein, self.custom_styles['Normal']))
        
        elements.append(Paragraph("Gehalt:", self.custom_styles['Label']))
        elements.append(Spacer(1, 0.5*cm))
        
        # Beruflicher Werdegang
        elements.append(Paragraph("Beruflicher Werdegang", self.custom_styles['Heading2']))
        
        # Berufserfahrungen hinzufügen
        for erfahrung in profile_data.get('berufserfahrung', []):
            # Zeitraum
            elements.append(Paragraph(f"Seit {erfahrung.get('zeitraum', '')}", self.custom_styles['Period']))
            
            # Unternehmen
            elements.append(Paragraph(erfahrung.get('unternehmen', ''), self.custom_styles['Company']))
            
            # Position/Rolle kursiv
            elements.append(Paragraph(erfahrung.get('position', ''), self.custom_styles['Position']))
            
            # Aufgaben als Aufzählung
            for aufgabe in erfahrung.get('aufgaben', []):
                elements.append(Paragraph(f"• {aufgabe}", self.custom_styles['Normal']))
            
            elements.append(Spacer(1, 0.5*cm))
        
        # Ausbildung
        elements.append(Paragraph("Ausbildung/ Weiterbildung", self.custom_styles['Heading2']))
        
        # Ausbildungen hinzufügen
        for ausbildung in profile_data.get('ausbildung', []):
            # Zeitraum
            elements.append(Paragraph(ausbildung.get('zeitraum', ''), self.custom_styles['Period']))
            
            # Institution
            elements.append(Paragraph(ausbildung.get('institution', ''), self.custom_styles['Company']))
            
            # Hinzufügen von Studienschwerpunkten, wenn vorhanden
            if ausbildung.get('schwerpunkte'):
                elements.append(Paragraph(f"Studienschwerpunkte: {ausbildung.get('schwerpunkte')}", self.custom_styles['Normal']))
            
            # Abschluss
            elements.append(Paragraph(f"Abschluss: {ausbildung.get('abschluss', '')}", self.custom_styles['Normal']))
            
            # Note wenn vorhanden
            if ausbildung.get('note'):
                elements.append(Paragraph(f"Abschlussnote {ausbildung.get('note')}", self.custom_styles['Normal']))
            
            elements.append(Spacer(1, 0.3*cm))
        
        # Weiterbildungen hinzufügen
        for weiterbildung in profile_data.get('weiterbildungen', []):
            # Zeitraum
            elements.append(Paragraph(weiterbildung.get('zeitraum', ''), self.custom_styles['Period']))
            
            # Bezeichnung
            elements.append(Paragraph(weiterbildung.get('bezeichnung', ''), self.custom_styles['Company']))
            
            # Abschluss wenn vorhanden
            if weiterbildung.get('abschluss'):
                elements.append(Paragraph(f"Abschluss: {weiterbildung.get('abschluss')}", self.custom_styles['Normal']))
            
            elements.append(Spacer(1, 0.3*cm))
        
        # Firmenfußzeile hinzufügen
        elements.append(Spacer(1, 1*cm))
        elements.append(self._create_footer())
        
        return elements
    
    def _create_horizontal_line(self):
        """Erstellt eine horizontale Linie als Tabelle"""
        return HRFlowable(width="100%", thickness=1, color=colors.lightgrey, spaceAfter=0.5*cm)
    
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
