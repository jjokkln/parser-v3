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
        
        # GALDORA Logo aus Bilddatei einbinden statt Text
        logo_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'galdoralogo.png')
        if os.path.exists(logo_path):
            img = Image(logo_path, width=180, height=60)
            elements.append(img)
            elements.append(Spacer(1, 1*cm))
        else:
            # Fallback wenn Bild nicht gefunden wurde
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
        # Layout mit zwei Spalten: linke Spalte leer, rechte Spalte für Ansprechpartner
        elements.append(Paragraph("IHR ANSPRECHPARTNER", self.custom_styles['ContactHeader']))
        
        # Kontaktinformationen
        kontakt = personal_data.get('kontakt', {})
        ansprechpartner = kontakt.get('ansprechpartner', 'Fischer')
        telefon = kontakt.get('telefon', '02161 62126-02')
        email = kontakt.get('email', 'fischer@galdora.de')
        
        # Erstelle Zwei-Spalten-Layout für Ansprechpartner (links leer, rechts Kontaktdaten)
        # Eine leere Spalte links und die Kontaktdaten rechts eingerückt
        contact_data = [
            ['', Paragraph(f"Herr {ansprechpartner}", self.custom_styles['Normal'])],
            ['', Paragraph(f"Telefon: {telefon}", self.custom_styles['Normal'])],
            ['', Paragraph(f"E-Mail: {email}", self.custom_styles['Normal'])]
        ]
        
        contact_table = Table(contact_data, colWidths=[180, 270])
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
        gehalt = personal_data.get('wunschgehalt', '')
        
        # Persönliche Daten als separate Zeilen mit Labels
        elements.append(Paragraph("Wohnort:", self.custom_styles['Label']))
        elements.append(Paragraph(wohnort, self.custom_styles['Normal']))
        
        elements.append(Paragraph("Jahrgang:", self.custom_styles['Label']))
        elements.append(Paragraph(jahrgang, self.custom_styles['Normal']))
        
        elements.append(Paragraph("Führerschein:", self.custom_styles['Label']))
        elements.append(Paragraph(führerschein, self.custom_styles['Normal']))
        
        elements.append(Paragraph("Gehalt:", self.custom_styles['Label']))
        # Ausgabe des Wunschgehalts, wenn vorhanden
        if gehalt:
            elements.append(Paragraph(gehalt, self.custom_styles['Normal']))
        elements.append(Spacer(1, 0.5*cm))
        
        # Beruflicher Werdegang
        elements.append(Paragraph("Beruflicher Werdegang", self.custom_styles['Heading2']))
        
        # Berufserfahrungen hinzufügen - im Zwei-Spalten-Layout
        for erfahrung in profile_data.get('berufserfahrung', []):
            # Zweispalten-Tabelle für Zeitraum (links) und Inhalt (rechts)
            zeitraum = erfahrung.get('zeitraum', '')
            position = erfahrung.get('position', '')
            unternehmen = erfahrung.get('unternehmen', '')
            
            # Linke Spalte: Zeitraum
            left_col = [Paragraph(f"{zeitraum}", self.custom_styles['Period'])]
            
            # Rechte Spalte: Unternehmen, Position und Aufgaben
            right_col_content = [
                Paragraph(unternehmen, self.custom_styles['Company']),
                Paragraph(position, self.custom_styles['Position'])
            ]
            
            # Aufgaben als Aufzählung - maximal 4 Aufgaben
            aufgaben = erfahrung.get('aufgaben', [])[:4]  # Begrenze auf max. 4 Aufgaben
            for aufgabe in aufgaben:
                right_col_content.append(Paragraph(f"• {aufgabe}", self.custom_styles['Normal']))
            
            right_col = [right_col_content]
            
            data = [[left_col, right_col]]
            
            table_style = TableStyle([
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('TOPPADDING', (0, 0), (-1, -1), 0),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
            ])
            
            # Erstelle Tabelle mit zwei Spalten
            experience_table = Table(data, colWidths=[100, 350])
            experience_table.setStyle(table_style)
            elements.append(experience_table)
            elements.append(Spacer(1, 0.5*cm))
        
        # Ausbildung
        elements.append(Paragraph("Ausbildung/ Weiterbildung", self.custom_styles['Heading2']))
        
        # Ausbildungen hinzufügen - im Zwei-Spalten-Layout
        for ausbildung in profile_data.get('ausbildung', []):
            # Zweispalten-Tabelle für Zeitraum (links) und Inhalt (rechts)
            zeitraum = ausbildung.get('zeitraum', '')
            institution = ausbildung.get('institution', '')
            abschluss = ausbildung.get('abschluss', '')
            schwerpunkte = ausbildung.get('schwerpunkte', '')
            note = ausbildung.get('note', '')
            
            # Linke Spalte: Zeitraum
            left_col = [Paragraph(f"{zeitraum}", self.custom_styles['Period'])]
            
            # Rechte Spalte: Institution und Details
            right_col_content = [
                Paragraph(institution, self.custom_styles['Company'])
            ]
            
            # Schwerpunkte wenn vorhanden
            if schwerpunkte:
                right_col_content.append(Paragraph(f"Studienschwerpunkte: {schwerpunkte}", self.custom_styles['Normal']))
            
            # Abschluss
            if abschluss:
                right_col_content.append(Paragraph(f"Abschluss: {abschluss}", self.custom_styles['Normal']))
            
            # Note wenn vorhanden
            if note:
                right_col_content.append(Paragraph(f"Abschlussnote {note}", self.custom_styles['Normal']))
            
            right_col = [right_col_content]
            
            data = [[left_col, right_col]]
            
            table_style = TableStyle([
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('TOPPADDING', (0, 0), (-1, -1), 0),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
            ])
            
            # Erstelle Tabelle mit zwei Spalten
            education_table = Table(data, colWidths=[100, 350])
            education_table.setStyle(table_style)
            elements.append(education_table)
            elements.append(Spacer(1, 0.3*cm))
        
        # Weiterbildungen hinzufügen - im Zwei-Spalten-Layout
        for weiterbildung in profile_data.get('weiterbildungen', []):
            # Zweispalten-Tabelle für Zeitraum (links) und Inhalt (rechts)
            zeitraum = weiterbildung.get('zeitraum', '')
            bezeichnung = weiterbildung.get('bezeichnung', '')
            abschluss = weiterbildung.get('abschluss', '')
            
            # Linke Spalte: Zeitraum
            left_col = [Paragraph(f"{zeitraum}", self.custom_styles['Period'])]
            
            # Rechte Spalte: Bezeichnung und Abschluss
            right_col_content = [
                Paragraph(bezeichnung, self.custom_styles['Company'])
            ]
            
            # Abschluss wenn vorhanden
            if abschluss:
                right_col_content.append(Paragraph(f"Abschluss: {abschluss}", self.custom_styles['Normal']))
            
            right_col = [right_col_content]
            
            data = [[left_col, right_col]]
            
            table_style = TableStyle([
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('TOPPADDING', (0, 0), (-1, -1), 0),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
            ])
            
            # Erstelle Tabelle mit zwei Spalten
            training_table = Table(data, colWidths=[100, 350])
            training_table.setStyle(table_style)
            elements.append(training_table)
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

# Überprüfungsfunktion zur Validierung der Profildaten
def check_missing_profile_data(profile_data):
    """
    Überprüft, ob alle wichtigen Informationen im Profil vorhanden sind
    
    Args:
        profile_data: Dictionary mit Profildaten
        
    Returns:
        Liste der fehlenden Schlüssel/Informationen
    """
    # Liste der erforderlichen Schlüssel
    required_keys = {
        'persönliche_daten': ['name', 'wohnort', 'jahrgang', 'führerschein', 'wunschgehalt'],
        'kontakt': ['ansprechpartner', 'telefon', 'email'],
        'berufserfahrung': [],  # Mindestens ein Eintrag sollte vorhanden sein
        'ausbildung': []        # Mindestens ein Eintrag sollte vorhanden sein
    }
    
    missing = []
    
    # Überprüfe persönliche Daten
    personal_data = profile_data.get('persönliche_daten', {})
    for key in required_keys['persönliche_daten']:
        if key not in personal_data or not personal_data[key]:
            missing.append(f"persönliche_daten.{key}")
    
    # Überprüfe Kontaktdaten
    kontakt = personal_data.get('kontakt', {})
    for key in required_keys['kontakt']:
        if key not in kontakt or not kontakt[key]:
            missing.append(f"persönliche_daten.kontakt.{key}")
    
    # Überprüfe, ob Berufserfahrung vorhanden ist
    if 'berufserfahrung' not in profile_data or not profile_data['berufserfahrung']:
        missing.append("berufserfahrung (mindestens ein Eintrag)")
    
    # Überprüfe, ob Ausbildung vorhanden ist
    if 'ausbildung' not in profile_data or not profile_data['ausbildung']:
        missing.append("ausbildung (mindestens ein Eintrag)")
    
    return missing
