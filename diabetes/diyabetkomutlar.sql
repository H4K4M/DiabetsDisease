CREATE TABLE Hasta(
	HastaID int NOT NULL IDENTITY,
	Ad nvarchar(255),
	Soyad nvarchar(255),
	Eposta nvarchar(255) UNIQUE,
	PRIMARY KEY (HastaID)
);

CREATE TABLE Test(
	TestID int NOT NULL IDENTITY,
	HastaID int FOREIGN KEY REFERENCES Hasta(HastaID),
	GebelikSayisi int,
	GlikozSeviyesi float,
	KanBasinci float,
	DeriKalinligi float,
	InsulinSeviyesi float,
	VucutKitleEndeksi float,
	DiyabetSoyagaci float,
	Yas int,
	Tarih date,
	Sonuc int
	PRIMARY KEY (TestID)
);

--Hasta Ekle Stored Procedure--
CREATE PROCEDURE HastaEkle @ad nvarchar(255), @soyad nvarchar(255), @eposta nvarchar(255)
AS
BEGIN
INSERT INTO Hasta
VALUES (@ad,@soyad,@eposta);
END

-- ÖRNEK 1 --
EXEC HastaEkle @ad='Eren', @soyad='Söme', @eposta = 'eren@some.com'

--Test Ekle Stored Procedure--
CREATE PROCEDURE TestEkle @hastaID int, @gebelik int, @glikoz float, @kan float, @deri float, @insulin float, @vke float, @soyagac float, @yas int, @tarih date, @sonuc int
AS
BEGIN
INSERT INTO Test
VALUES (@hastaID, @gebelik, @glikoz, @kan, @deri, @insulin, @vke, @soyagac, @yas, @tarih, @sonuc);
END

-- ÖRNEK 2 --
EXEC TestEkle @hastaID=1, @gebelik=0, @glikoz=137, @kan=20, @deri=35, @insulin=168, @vke=43.1, @soyagac=2.288, @yas=22, @sonuc=0


--HastaTestGetir Stored Procedure--
CREATE PROCEDURE HastaTestGetir @eposta nvarchar(255)
AS
BEGIN
SELECT  t.TestID as 'Test Numarasý', h.Ad + ' ' + h.Soyad as 'Ad Soyad', t.Tarih as 'Test Tarihi', t.Sonuc as 'Test Sonucu'
FROM Hasta h, Test t
WHERE t.HastaID = h.HastaID
ORDER BY t.Tarih DESC
END

-- ÖRNEK 3 --
EXEC HastaTestGetir @eposta = 'huseyink@gmail.com'


--BelirtilenSonucTestGetir--
CREATE PROCEDURE BelirtilenSonucTestGetir @sonuc int
AS
BEGIN
SELECT t.TestID as 'Test Numarasý', h.Ad + ' ' + h.Soyad as 'Ad Soyad', t.Tarih as 'Test Tarihi', t.Sonuc as 'Test Sonucu'
FROM Hasta h, Test t
WHERE t.HastaID = h.HastaID AND t.Sonuc = @sonuc
ORDER BY 'Ad Soyad', t.Tarih DESC
END


-- ÖRNEK 4 --
EXEC BelirtilenSonucTestGetir @sonuc = 1

--Test_Tarih Trigger--
CREATE TRIGGER Test_Tarih
ON Test
AFTER INSERT
AS
BEGIN
	UPDATE Test
	SET Tarih = GETDATE()
	WHERE Tarih IS NULL;
END